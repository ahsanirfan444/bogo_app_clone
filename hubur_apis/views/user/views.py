from django.forms import ValidationError
from rest_framework.response import Response
from rest_framework import serializers
from hubur_apis import models
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

from hubur_apis.serializers.user_serializer import (
    CitySerializer,
    CountrySerializer,
    ForgotPasswordSerializer,
    GetUserProfileSerializer,
    EmailLoginSerializer,
    NotificationSettingsSerializer,
    ResetPasswordSerializer,
    UserProfileSerializer,
    VerifyUserSerializer,
    ChangePassAfterVerifySerializer,
    ResendCodeSerializer,
    ContactLoginSerializer
)

class CustomAuthLogin(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        lang_code = request.headers.get('Accept-Language')
        req = request.data
        response = super(CustomAuthLogin, self).post(request, *args, **kwargs)
        res = response.data
        token = res.get('token')
        if 'password' in req:
            if 'email'in req and 'type' in req :
                email_user_serializer = EmailLoginSerializer(data=request.data)
                if email_user_serializer.is_valid():
                    del email_user_serializer.validated_data['password'], email_user_serializer.validated_data['type']
                    user = models.UserProfile.objects.get(**email_user_serializer.validated_data)
                    if user.role == 2 or user.role == 3 or user.role == 4:
                        return Response({'error': ['Incorrect email or password'], 'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
                    
                    user.lang_code = lang_code
                    user.save()
                    if token:
                        valid_data = VerifyJSONWebTokenSerializer().validate(response.data)
                        user = valid_data['user']
                    else:
                        return Response({'error': ['Incorrect email or password'], 'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    error_list = []
                    for e in email_user_serializer.errors.values():
                        error_list.append(e[0])
                    return Response({'error': error_list, 'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

            elif 'contact' in req  and 'country_code' in req and 'type' in req :

                contact_user_serializer = ContactLoginSerializer(data=request.data)
                if contact_user_serializer.is_valid():
                    del contact_user_serializer.validated_data['password'], contact_user_serializer.validated_data['type']
                    user = models.UserProfile.objects.get(**contact_user_serializer.validated_data)
                    user.lang_code = lang_code
                    user.save()
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
                    response.data['token'] = token
                else:
                    error_list = []
                    for e in contact_user_serializer.errors.values():
                        error_list.append(e[0])
                    return Response({'error': error_list, 'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if 'type' not in req:
                    return Response({'error':["type is missing"] , 'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error':["contact detail is missing"] , 'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':["password is missing"] , 'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        user_interest_list = models.UserInterest.objects.filter(i_user=user).values('id','i_category__name')

        user_serializer = GetUserProfileSerializer(user, context={"request": request})
        user_data = user_serializer.data
        user_data['interest'] = user_interest_list
        dict1 = dict(user_data)
        dict2 = dict(res)
        response_data = {**dict2, **dict1}
        
        return Response({'error': [], 'error_code': '', 'data': [response_data], 'status': status.HTTP_200_OK, }, status=status.HTTP_200_OK)
    
class UserProfileViewSet(viewsets.ModelViewSet):
    """ Creating and updating user profile """

    serializer_class = UserProfileSerializer
    queryset = models.UserProfile.objects.filter(is_active=True)

    def create(self, request, *args, **kwargs):

        error_list = []
        try:

            serializer = self.get_serializer(data=request.data)
            validation = serializer.is_valid()

            if validation:
                if 'apple' in serializer.validated_data:
                    del serializer.validated_data['apple']
                self.perform_create(serializer)

                returnObj = serializer.data
                if returnObj['is_type'] == 2:
                    user_obj = models.UserProfile.objects.get(id=returnObj['id'])
                    user_obj.is_active = True
                    user_obj.is_verified = True
                    user_obj.save()
                    if 'apple' in request.data:
                        models.AppleToken.objects.create(i_user=user_obj, token = request.data['apple'])
                    payload = jwt_payload_handler(user_obj)
                    token = jwt_encode_handler(payload)
                    returnObj['token'] = token

                return Response({'error': [], 'error_code': '', 'data': [returnObj], 'status': status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
    
            for e in serializer.errors.values():
                error_list.append(e[0])
            return Response({'error': error_list, 'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            error_list.append(repr(e))
        return Response({'error': error_list, 'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):

        if models.UserProfile.objects.filter(email=serializer.validated_data['email']).exists():
            raise serializers.ValidationError(
                {"email": "This email address is already registered with this role."})

        else:
            serializer.save()

    def update(self, request, pk, *args, **kwargs):
        inst = models.UserProfile.objects.get(id=pk)
        user = pk

        if "email" in request.data:
            
            email = request.data.get("email")
            try:
                emailInst = models.UserProfile.objects.get(email=email)
                if inst.email != emailInst.email:
                    return Response({'error': ['Email already exists'], 'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return super().update(request, pk, *args, **kwargs)
                    
            except models.UserProfile.DoesNotExist:
                return super().update(request, pk, *args, **kwargs)
        return super().update(request, pk, *args, **kwargs)

    def perform_update(self, serializer):
        if self.request.user.username:
            if "profile_picture" in serializer.validated_data:
                if self.request.user.profile_picture:
                    self.request.user.profile_picture.delete()
            serializer.save()
        else:
            raise serializers.ValidationError({'error': ['No User Login'],'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST})

    def retrieve(self, request, pk=None):
        queryset = models.UserProfile.objects.filter(is_active=True)
        obj = get_object_or_404(queryset, pk=pk)
        serializer = GetUserProfileSerializer(obj, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        all_countries_list = list(models.Country.objects.filter(is_active=True).values_list("id",flat=True))
        all_cities_list = list(models.City.objects.filter(is_active=True).values_list("id",flat=True))
        
        queryset = models.UserProfile.objects.filter(id=request.user.id)
        error_list = []
        data = get_object_or_404(queryset, pk=pk)
        if 'i_city' in request.data:
            i_city = int(request.data.get('i_city'))
            if i_city in all_cities_list:
                data.i_city_id = i_city
                data.save()
            else:
                raise serializers.ValidationError({'error': ['No City Found'],'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST})
        if 'i_country' in request.data:
            i_country = int(request.data.get('i_country'))
            if i_country in all_countries_list:
                data.i_country_id = i_country
                data.save()
            else:
                raise serializers.ValidationError({'error': ['No Country Found'],'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST})
        if ('old_password' or 'new_password' or 'password') in request.data:
            context = {"user": request.user}
            change_pass_serializer = ResetPasswordSerializer(data=request.data, context=context)
            if change_pass_serializer.is_valid():
                serializer = GetUserProfileSerializer(data, context={"request": request}, data=request.data, partial=True)
                if serializer.is_valid():
                    password = change_pass_serializer.validated_data['password']
                    data.set_password(password)
                    data.save()
                    serializer.save()
                    return Response(serializer.data,  status=status.HTTP_200_OK)
                else:
                    for e in serializer.errors.values():
                        error_list.append(e[0])
            else:
                for e in change_pass_serializer.errors.values():
                    error_list.append(e[0])
        else:
            serializer = GetUserProfileSerializer(data, context={"request": request}, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,  status=status.HTTP_200_OK)
            else:
                for e in serializer.errors.values():
                    error_list.append(e[0])

        return Response({'error': error_list, 'error_code': 'HS002', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

            

class UserStatusAPIView(APIView):
    def get(self, request,pk, *args, **kwargs):
        if pk:
            user_data = {}
            queryset = models.UserProfile.objects.filter(is_active=True, role=1)
            obj = get_object_or_404(queryset, pk=pk)
            if obj:
                if request.user.is_authenticated:
                    serializer = GetUserProfileSerializer(obj, context={"user_obj":request.user, "request": request})
                else:
                    serializer = GetUserProfileSerializer(obj, context={"request": request})
                user_data = serializer.data
                return Response({'error': [], 'error_code': '', 'data': [user_data], 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        
        return Response({'error': ['No user found'], 'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    

class AppleLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
            
        if 'token' in request.data:
            token = request.data['token']
            token_obj = models.AppleToken.objects.filter(token=token)
            if token_obj.exists():
                user_obj = token_obj[0].i_user
                if user_obj.is_active == False and user_obj.is_verified:
                    return Response({'error': ["You're temporary Blocked by Admin"], 'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    payload = jwt_payload_handler(user_obj)
                    token = jwt_encode_handler(payload)
                    user_interest_list = models.UserInterest.objects.filter(i_user=user_obj).values('id','i_category__name')
    

                    user_serializer = GetUserProfileSerializer(user_obj, context={"request": request})
                    user_data = user_serializer.data
                    user_data['interest'] = user_interest_list
                    dict1 = dict(user_data)
                    dict2 = dict({'token':token})
                    response_data = {**dict2, **dict1}

                    return Response({'error': [], 'error_code': '', 'data': [response_data], 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)

    
        return Response({'error': ['No user found'], 'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

class ChangeNotificationSettingAPIView(APIView):
    def patch(self, request, format=None):
        try:
            instance = request.user
            notification_settings = models.NotificationSettings.objects.get(i_user=instance)
            serializer = NotificationSettingsSerializer(data=request.data)
            # if 
            if serializer.is_valid():
                if request.data and list(request.data)[0] in serializer.data.keys():
                    if request.data.get('all_notifications') == str(False):
                        notification_settings.all_notifications = False
                        notification_settings.new_offer = False
                        notification_settings.offer_expire = False
                        notification_settings.save()
                    else:
                        notification_settings.update_on_whatsapp = request.data.get('update_on_whatsapp', notification_settings.update_on_whatsapp)
                        notification_settings.promotional_messages = request.data.get('promotional_messages', notification_settings.promotional_messages)
                        notification_settings.promotional_email = request.data.get('promotional_email', notification_settings.promotional_email)
                        notification_settings.all_notifications = request.data.get('all_notifications', notification_settings.all_notifications)
                        notification_settings.new_offer = request.data.get('new_offer', notification_settings.new_offer)
                        notification_settings.offer_expire   = request.data.get('offer_expire', notification_settings.offer_expire)
                        notification_settings.save()
                    return Response({'error': [], 'error_code': '', 'data': ['Notification Settings updated successfully'], 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': ['Nothing to update'], 'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
                    
            else:
                return Response({'error': [], 'error_code': '', 'data': ['Notification Settings updated Failed'], 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except ValidationError:
            return Response({'error': ['Value should be True or False'], 'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            

class UserStatusTokenAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user_data = {}
        try:
            obj = models.UserProfile.objects.get(is_active=True, id=request.user.id)
        except:
            return Response({'error': ['No user found'], 'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        if obj:
            serializer = GetUserProfileSerializer(obj, context={"user_obj":request.user, "request": request})
            
            user_data = serializer.data
            return Response({'error': [], 'error_code': '', 'data': [user_data], 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    
class VerifyUser(APIView):

    def post(self, request, *args, **kwargs):
        try:
            verify_otp_serializer = VerifyUserSerializer(
                data=request.data)
            if verify_otp_serializer.is_valid():
                verify_otp_serializer.save()
                if verify_otp_serializer.instance['status'] == 'verified':

                    user = verify_otp_serializer.instance['user']

                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
                    response = dict()
                    response['message'] = 'Successfully Verified'
                    response['token'] = token


                    return Response({'error': [], 'error_code': '', 'message': [response], 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)

                elif verify_otp_serializer.instance['status'] == 'expired':
                    return Response({'error': ['OTP is Expired'], 'error_code': '', 'message': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': ['Invalid OTP'], 'error_code': '', 'message': [], 'status': status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                error_list = []
                for e in verify_otp_serializer.errors.values():
                    error_list.append(e[0])
                return Response({'error': error_list, 'error_code': 'HS002', 'message': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            error_list = [repr(error)]
            return Response({'error': error_list, 'error_code': 'H007', 'matched': 'N', 'message': [], 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResetPassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            context = {"user": request.user}
            change_pass_serializer = ResetPasswordSerializer(
                data=request.data, context=context)
            if change_pass_serializer.is_valid():
                change_pass_serializer.save()
                return Response(
                    {'error': [], 'error_code': '', 'data': ["Password Successfully Change"], 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                error_list = []
                for e in change_pass_serializer.errors.values():
                    error_list.append(e[0])
                return Response({'error': error_list, 'error_code': 'HS002', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            error_list = [repr(error)]
            return Response({'error':error_list , 'error_code': 'H007', 'matched': 'N', 'data': [], 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ForgotPassword(APIView):

    def post(self, request, *args, **kwargs):
        try:
            otp_serializer = ForgotPasswordSerializer(data=request.data)
            if otp_serializer.is_valid():
                otp_serializer.save()
                return Response(
                    {'error': [], 'error_code': '', 'message': ['OTP code has been sent'], 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                error_list = []
                for e in otp_serializer.errors.values():
                    error_list.append(e[0])
                return Response({'error': error_list, 'error_code': 'HS002', 'message': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            error_list = [repr(error)]
            return Response({'error': error_list, 'error_code': 'H007', 'matched': 'N', 'message': [], 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResendCodeAPI(APIView):

    def post(self, request, *args, **kwargs):
        try:
            otp_serializer = ResendCodeSerializer(data=request.data)
            if otp_serializer.is_valid():
                otp_serializer.save()
                return Response(
                    {'error': [], 'error_code': '', 'message': ['OTP code has been sent'], 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                error_list = []
                for e in otp_serializer.errors.values():
                    error_list.append(e[0])
                return Response({'error': error_list, 'error_code': 'HS002', 'message': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'error': [repr(error)], 'error_code': 'H007', 'matched': 'N', 'message': [], 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChangePassAfterVerify(APIView):

    def post(self, request, *args, **kwargs):
        try:
            serializer = ChangePassAfterVerifySerializer(
                data=request.data)
            if serializer.is_valid():
                serializer.save()
                if serializer.instance['status'] == True:
                    return Response({'error': [], 'error_code': '', 'message': ['Password Successfully Changed'], 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
                elif serializer.instance['status'] == False:
                    return Response({'error': ['No User Found'], 'error_code': '', 'message': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
                elif serializer.instance['status'] == 'expired':
                    return Response({'error': ['OTP is Expired'], 'error_code': '', 'message': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
                elif serializer.instance['status'] == 'Null':
                    return Response({'error': ['Incorrect OTP'], 'error_code': '', 'message': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': ['Something went wrong'], 'error_code': '', 'message': [], 'status': status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                error_list = []
                for e in serializer.errors.values():
                    error_list.append(e[0])
                return Response({'error': error_list, 'error_code': 'HS002', 'message': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'error': repr(error), 'error_code': 'H007', 'matched': 'N', 'message': [], 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SaveLocatonView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            user_id = request.user.id
            lat = float(request.data['lat'])
            long = float(request.data['long'])
            if lat and long:
                user_obj = models.UserProfile.objects.get(id=user_id)
                user_obj.long = long
                user_obj.lat = lat
                user_obj.save()
                return Response({'error': [], 'error_code': '', 'message': ['Location Save'], 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': ['Please Enter Latitude and Longitude'], 'error_code': '', 'message': [], 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'error': [repr(error)], 'error_code': 'H007', 'matched': 'N', 'message': [], 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetAllCitiesViewSet(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    queryset = models.City.objects.filter(is_active=True)


    def retrieve(self, request, pk=None):
        country = models.Country.objects.filter(is_active=True)
        data = get_object_or_404(country, pk=pk)
        if data:
            cities = models.City.objects.filter(i_country=pk)
        
            serializer = CitySerializer(cities, context={"request": request}, many=True)
            return Response({'error': [], 'error_code': '', 'data': serializer.data, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': [], 'error_code': '', 'data': ["No Country found"], 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    

    def list(self, request, *args, **kwargs):
        queryset = models.Country.objects.filter(is_active=True)
        serializer = CountrySerializer(queryset, context={"request": request}, many=True)

        return Response({'error': [], 'error_code': '', 'data': serializer.data, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)

class UserOnlineStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            obj = models.UserProfile.objects.get(is_active=True, id=request.user.id)
        except:
            return Response({'error': ['No user found'], 'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        user_online_status = models.UserOnlineStatus.objects.filter(i_user=obj)
        if user_online_status.exists():
            user_online_status = user_online_status.first()
            if user_online_status.is_online:
                user_online_status.is_online = False
                user_online_status.save()
                return Response({'error': [], 'error_code': '', 'data': ["Offline successfully"], 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                user_online_status.is_online = True
                user_online_status.save()
                return Response({'error': [], 'error_code': '', 'data': ["Online successfully"], 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            models.UserOnlineStatus.objects.create(i_user=obj, is_online=True)
            return Response({'error': [], 'error_code': '', 'data': ["Online successfully"], 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
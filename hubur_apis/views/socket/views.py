from math import ceil
from django.urls import reverse_lazy
from rest_framework.response import Response
from core.defaults import DefualtPaginationClass
from global_methods import distance
from hubur_apis import models
from rest_framework import status, viewsets, filters, views,permissions
from hubur_apis.serializers.chat_serializer import CreateMessagesSerializer, UserInfoForChatSerializer
from hubur_apis.serializers.home_serializer import LocationForGuestModeSerializer
from hubur_apis.serializers.search_serializer import  GetBusinessSerializer
from hubur_apis.serializers.story_serializer import BusinessLogoSerializer
from hubur_apis.serializers.socket_serializer import (
    MapBusinessSerializer, SocketSerializer,SearchBusinessInMapSerializer)
from concurrent.futures import ThreadPoolExecutor
from django.db.models import Q,Case, When
import notifications
from hubur_apis.views.web_socket.connection import connect

class SocketData(viewsets.ModelViewSet):

    serializer_class = SocketSerializer
    queryset = models.Business.objects.filter(is_active=True).exclude(i_user__is_active=False).order_by('-created_at')

    def create(self,request):
            socket_serializer = SocketSerializer(data=request.data)
            if socket_serializer.is_valid():
                user_long = socket_serializer.validated_data['long']
                user_lat = socket_serializer.validated_data['lat']
                all_businesses_objs = []
                if 'i_subcategory' in socket_serializer.validated_data and socket_serializer.validated_data['i_subcategory'] != None:
                    i_subcategory = socket_serializer.validated_data['i_subcategory']
                    business_obj = models.Business.objects.filter(is_active=True,i_subcategory=i_subcategory).exclude(i_user__is_active=False).prefetch_related('i_category', 'i_user')
                    
                else:
                    business_obj = models.Business.objects.filter(is_active=True).exclude(i_user__is_active=False).prefetch_related('i_category', 'i_user')
                for bus in business_obj:
                    dis = distance(user_lat,user_long,bus.lat,bus.long)
                    if float(dis) <= 10:
                        all_businesses_objs.append(bus)
                        
                context = {'user_long': user_long,'user_lat':user_lat}
                map_business_serializer = MapBusinessSerializer(all_businesses_objs,context=context ,many=True)
                map_business_serializer = sorted(map_business_serializer.data, key=lambda x: x['total_distance'])

                all_businesses = []
                max_workers = 10

                def map_serializer(business):
                    return business
                
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    results = executor.map(map_serializer, map_business_serializer)
                    for result in results:
                        if result is not None:
                            all_businesses.append(result)
                            if len(all_businesses) == 150:
                                break
                
                if all_businesses:
                    return Response({'error': [], 'error_code': '', 'data': all_businesses,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': [], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': socket_serializer.errors, 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

            
    def list(self, request, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
       
    def perform_update(self, serializer):
       return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, pk=None):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
class SearchForMapAPIView(viewsets.ModelViewSet):

    serializer_class = GetBusinessSerializer
    queryset = models.Business.objects.filter(is_active=True).exclude(i_user__is_active=False)
    filter_backends = [filters.SearchFilter]
    pagination_class = DefualtPaginationClass
    search_fields = ['^name','name','^i_subcategory__name']

    def list(self,request):
        
        user_long = 0
        user_lat = 0
        if 'long' and 'lat' in request.GET:
            location_serializer = LocationForGuestModeSerializer(data=request.GET)
            if location_serializer.is_valid():
                user_long = location_serializer.data['long']
                user_lat = location_serializer.data['lat']
                if request.user.username:
                    
                    updates = {'long': user_long, 'lat': user_lat}
                    models.UserProfile.objects.filter(id=request.user.id).update(**updates)
            else:
                error_list = []
                for e in location_serializer.errors.values():
                    error_list.append(e[0])
                return Response({'error': error_list, 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        elif request.user.username:
            user_long = request.user.long
            user_lat = request.user.lat

        if 'sub_id' in request.GET:
            sub_catagories_list = list(models.SubCategories.objects.filter(is_active=True).values_list('id',flat=True))
            sub_id = request.GET['sub_id']
            if int(sub_id) in sub_catagories_list:
                business_query_filtered = models.Business.objects.filter(is_active=True, i_subcategory__id=sub_id).exclude(i_user__is_active=False)
            else:
                return Response({'error': ["No Result Found"], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        elif 'search_key' in request.GET:
            if request.GET['search_key'] == "Trending":
                business_id_list = list(models.PopularSearch.objects.filter(is_active=True, type="Business").exclude(Q(i_brand__isnull=False) | Q(i_content__isnull=False)).values_list('i_business',flat=True).order_by("-count"))
                business_query_filtered = models.Business.objects.filter(is_active=True, id__in=business_id_list).exclude(i_user__is_active=False)

                if business_query_filtered:
                    id_dict = {id_val: pos for pos, id_val in enumerate(business_id_list)}
                    whens = [When(id=id_val, then=pos) for id_val, pos in id_dict.items()]
                    order_by = Case(*whens)
                    business_query_filtered = business_query_filtered.order_by(order_by)

            elif request.GET['search_key'] == "Visited":
                if request.user.username:
                    business_id_list = list(models.Visited.objects.filter(i_user=request.user).values_list('i_business_id',flat=True).order_by("-created_at"))
                    business_query_filtered = models.Business.objects.filter(is_active=True, id__in=business_id_list).exclude(i_user__is_active=False)
                    if business_query_filtered:
                        id_dict = {id_val: pos for pos, id_val in enumerate(business_id_list)}
                        whens = [When(id=id_val, then=pos) for id_val, pos in id_dict.items()]
                        order_by = Case(*whens)
                        business_query_filtered = business_query_filtered.order_by(order_by)
                else:
                    return Response({'error': ["No User Found"], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            
            elif request.GET['search_key'] == "Saved":
                if request.user.username:
                    business_id_list = list(models.MyBookmark.objects.filter(i_user=request.user).values_list('i_business_id',flat=True).order_by("-created_at"))
                    business_query_filtered = models.Business.objects.filter(is_active=True, id__in=business_id_list).exclude(i_user__is_active=False)
                    if business_query_filtered:
                        id_dict = {id_val: pos for pos, id_val in enumerate(business_id_list)}
                        whens = [When(id=id_val, then=pos) for id_val, pos in id_dict.items()]
                        order_by = Case(*whens)
                        business_query_filtered = business_query_filtered.order_by(order_by)
                else:
                    return Response({'error': ["No User Found"], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
                    
            else:
                return Response({'error': ["No search_key Found"], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)

        else:
            business_query_filtered = models.Business.objects.filter(is_active=True).exclude(i_user__is_active=False).prefetch_related('i_category', 'i_user')

        business_query = business_query_filtered
        business_query = self.filter_queryset(business_query)

        all_businesses_objs = [bus for bus in business_query if float(distance(user_lat, user_long, bus.lat, bus.long)) <= 10][:200]

        
                
        context = {'user_long': user_long,'user_lat':user_lat}
        map_business_serializer = SearchBusinessInMapSerializer(all_businesses_objs,context=context ,many=True)
        map_business_serializer = sorted(map_business_serializer.data, key=lambda x: x['total_distance'])


        max_workers = 10

        def map_serializer(business):
            return business
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = executor.map(map_serializer, map_business_serializer)
            results = [result for result in results if results is not None]
            all_businesses_list = [bus for bus in results][:100]
            

        if all_businesses_list:
            return Response({'error': [], 'error_code': '', 'data': all_businesses_list,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': ["No Data Found "], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
                
    def create(self, request, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
       
    def perform_update(self, serializer):
       return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, pk=None):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CreateMessagesUsingSocket(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        context = {"user_ob":request.user}
        serializer = CreateMessagesSerializer(data=request.data, context=context)
        if serializer.is_valid():
            models.Message.objects.create(**serializer.validated_data)
            data = dict()
            data['last_message'] = serializer.validated_data['content']
            data['user_1_id'] = serializer.validated_data['receiver_id']
            data['channel_id'] = serializer.validated_data['channel_id']
            data['user_2'] = serializer.validated_data['sender']
            data['count'] = 1
            chat = models.Chat.objects.filter(channel_id=data['channel_id'])
            if chat.exists():
                chat = chat.first()
                chat.last_message = data['last_message']
                chat.count = chat.count + 1
                chat.is_read = False
                chat.save()
            else:

                models.Chat.objects.create(**data)
            
            title =f"{data['user_2'].get_name()}"
            msg = data['last_message']
            if 'Product Sent' in msg:
                msg = "Product shared with you"
            elif 'Business Sent' in msg:
                msg = "Business shared with you"
            elif 'Profile Sent' in msg:
                msg = "Profile shared with you"
            elif 'Story Sent' in msg:
                msg = "Story shared with you"
            else:
                msg
            
            business = models.Business.objects.filter(i_user=request.user.id)
            if business.exists():
                business = business.first()
                sender_name = business.name
                sender_pic = BusinessLogoSerializer(business).data['logo_pic']
                business_id = str(business.id)
            else:
                
                sender_name = request.user.get_name()
                sender_pic = UserInfoForChatSerializer(request.user).data['profile_picture']
                business_id = ""

            sender_type = request.user.get_role_display()
            receiver_type = models.UserProfile.objects.get(id=data['user_1_id']).role
            sender_user_id = str(request.user.id)
            channel_id = data['channel_id']

            if receiver_type == 2:
                notifications.sendNotificationToVendor(data['user_1_id'], msg, title, request.user.id, 3, self.request.build_absolute_uri(reverse_lazy("chat_detail", kwargs={"user_id": int(request.user.id)})))
            else:

                notifications.sendNotificationToSingleUser(data['user_1_id'], msg, None, title, None, request.user.id, None, None,notification_type=3, activityAndroid="FLUTTER_NOTIFICATION_CLICK", activityIOS="FLUTTER_NOTIFICATION_CLICK",code=None ,sender_name=sender_name, 
                                                       business_id=business_id,sender_type=sender_type,sender_pic=sender_pic,channel_id=channel_id,type="Chat",sender_user_id=sender_user_id)

            
            return Response({'error': [], 'error_code': '', 'data': "saved message",'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            error_list = []
            for e in serializer.errors.values():
                error_list.append(e[0])
            return Response({'error': error_list, 'error_code': '', 'data': "",'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


class HitSocketForSharing(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        context = {"user_ob":request.user}

        serializer = CreateMessagesSerializer(data=request.data, context=context)
        if serializer.is_valid():
            data = request.data
            socket_url = data['socket_url']

            data['token'] = request.headers['Authorization'].split(" ")[1]
            del data['socket_url']
            data = dict(data)

            connect(data,socket_url)


            return Response({'error': [], 'error_code': '', 'data': "saved message",'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)

        else:
            error_list = []
            for e in serializer.errors.values():
                error_list.append(e[0])
            return Response({'error': error_list, 'error_code': '', 'data': "",'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)



from datetime import datetime, timedelta, timezone
from rest_framework import serializers
from hubur_apis import models
import django.contrib.auth.password_validation as validators
from django.core import exceptions
import global_methods, notifications
from django.db.models import Q
from global_methods import format_number

class NotificationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NotificationSettings
        fields = ('update_on_whatsapp','promotional_messages','promotional_email','all_notifications','new_offer','offer_expire',)

class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture = global_methods.Base64ImageField(required=False, default='profile_pictures/logo_min.png')
    city_name = serializers.SerializerMethodField()
    country_name = serializers.SerializerMethodField()
    apple = serializers.CharField(required=False)

    class Meta:
        model = models.UserProfile
        fields = ('id', 'first_name', 'last_name', 'email', 'contact', 'profile_picture', 'password', 'dob', 'is_type', 'address', 'country_code', 'gender', 'terms_conditions', 'i_city', 'i_country', 'bg_image','city_name','country_name','apple', 'lang_code',)
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
            'id': {
                "read_only": True,
            },
            'apple': {
                "read_only": True,
            },
        }

    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context.get('request')
        response['voting'] = format_number(models.Voting.objects.filter(i_user=instance, i_business__is_active=True).exclude(i_business__i_user__is_active=False).count())
        response['checkins'] = format_number(models.Checkedin.objects.filter(i_user=instance, is_active=True, i_business__is_active=True).exclude(i_business__i_user__is_active=False).count())
        response['my_favorites'] = format_number(models.MyFavourite.objects.filter(i_user=instance).exclude(Q(i_business__i_user__is_active=False) | Q(i_content__i_brand__is_active=False) | Q(i_business__is_active=False) | Q(i_content__is_active=False) | Q(i_content__i_sub_category__is_active=False)).count())
        response['my_booking'] = format_number(models.Booking.objects.filter(i_user=instance, i_business__is_active=True).exclude(i_business__i_user__is_active=False).count())
        response['my_bookmark'] = format_number(models.MyBookmark.objects.filter(i_user=instance, i_business__is_active=True).exclude(i_business__i_user__is_active=False).count())
        response['my_reviews'] = format_number(models.Reviews.objects.filter(i_user=instance).exclude( Q(i_content__i_brand__is_active=False) | Q(i_content__i_sub_category__is_active=False) | Q(i_business__i_user__is_active=False) | Q(i_content__is_active=False) | Q(i_business__is_active=False)).count())
        response['my_saved_offer'] = format_number(models.SavedOffers.objects.filter(i_user=instance, i_business__is_active=True, i_content__is_active=True, i_content__i_sub_category__is_active=True).exclude(Q(i_business__i_user__is_active=False) | Q(i_content__i_brand__is_active=False)).count())
        response['my_friends'] = format_number(models.FriendList.objects.filter(i_user=instance, friends__is_active=True, is_active=True).count())
        response['my_rewards'] = format_number(models.UserReward.objects.filter(i_user=instance).count())
        notification_setting_obj = models.NotificationSettings.objects.create(i_user=instance)
        response['notification_settings'] = NotificationSettingsSerializer(notification_setting_obj).data
        try:
            response['i_city'] = instance.i_city.name if request.user.lang_code == 1 else instance.i_city.name_ar
            response['i_country'] = instance.i_country.name if request.user.lang_code == 1 else instance.i_country.name_ar
        except Exception:
            response['i_city'] = instance.i_city.name if request.headers.get('Accept-Language') == str(1) else instance.i_city.name_ar
            response['i_country'] = instance.i_country.name if request.headers.get('Accept-Language') == str(1) else instance.i_country.name_ar
        return response
  
    def get_city_name(self, obj):
        if obj.i_city:
            return obj.i_city.name
        else:
            return ""
    
    def get_country_name(self, obj):
        if obj.i_country:
            return obj.i_country.name
        else:
            return ""
    
    def get_full_url(self):
        request = self.context.get('request')
        url = models.UserProfile.profile_picture.url
        return request.build_absolute_uri(url)

    def validate(self, data):
        if 'apple' in data:
            if models.AppleToken.objects.filter(token=data['apple']).exists():
                raise serializers.ValidationError("user profile with this contact already exists")
        password = data.get('password')
        errors = dict()
        try:
            validators.validate_password(password=password)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)

        return super(UserProfileSerializer, self).validate(data)

    def create(self, validated_data):
        """ Creates and returns the new User """
        user = None
        request = self.context.get('request')
        medium = request.data.get('medium')
        is_type = request.data.get('is_type')

        code_dict = global_methods.generate_otp_tokens()
        email_address = validated_data['email']
        subject = 'OTP for hubur'
        html_message = "Your otp verification code is %s " % code_dict['email_code']

        if ('country_code' in validated_data) and ('+' in validated_data['country_code']):
            validated_data['country_code'] = validated_data['country_code'].replace("+","")

        email = validated_data.get('email')
        username = email.split('@')[0]
        validated_data['username'] = username

        if medium == '1':
            user = models.UserProfile.objects.create_user(**validated_data)
            user.set_password(validated_data.get('password'))
            user.save()
            if is_type == '1':
                sms_message = "Your otp verification code is %s " % code_dict['sms_code']
                models.OtpToken.objects.create(i_user=user,code=code_dict['sms_code'],medium = "1")
                contact_no = "+"+str(validated_data['country_code']+validated_data['contact'])
                notifications.sendMessageToSingleUser(sms_message,contact_no)
            return user
        elif medium == '2':
            if "gender" not in validated_data or validated_data['gender'] is None:
                validated_data['gender'] = 1
            user = models.UserProfile.objects.create_user(**validated_data)
            user.set_password(validated_data.get('password'))
            user.save()
            if is_type == '1':
                notifications.sendEmailToSingleUser(html_message, email_address, subject)
                models.OtpToken.objects.create(i_user=user,code=code_dict['email_code'],medium = "2")
            return user
        
    def update(self, instance, validated_data):

        if "password" in validated_data:
            password = validated_data.pop("password")

            instance.set_password(password)

        return super().update(instance, validated_data)

class GetUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('id','first_name','last_name','username','email','contact','i_city','i_country','profile_picture','dob','country_code','address','is_verified','long','lat','is_type','gender','terms_conditions','bg_image','is_active', 'lang_code',)
        

    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context.get('request')
        response['voting'] = format_number(models.Voting.objects.filter(i_user=instance, i_business__is_active=True).exclude(i_business__i_user__is_active=False).count())
        response['checkins'] = format_number(models.Checkedin.objects.filter(i_user=instance, is_active=True, i_business__is_active=True).exclude(i_business__i_user__is_active=False).count())
        response['my_favorites'] = format_number(models.MyFavourite.objects.filter(i_user=instance).exclude(Q(i_business__i_user__is_active=False) | Q(i_content__i_brand__is_active=False) | Q(i_business__is_active=False) | Q(i_content__is_active=False) | Q(i_content__i_sub_category__is_active=False)).count())
        response['my_booking'] = format_number(models.Booking.objects.filter(i_user=instance, i_business__is_active=True).exclude(i_business__i_user__is_active=False).count())
        response['my_bookmark'] = format_number(models.MyBookmark.objects.filter(i_user=instance, i_business__is_active=True).exclude(i_business__i_user__is_active=False).count())
        response['my_reviews'] = format_number(models.Reviews.objects.filter(i_user=instance).exclude( Q(i_content__i_brand__is_active=False) | Q(i_content__i_sub_category__is_active=False) | Q(i_business__i_user__is_active=False) | Q(i_content__is_active=False) | Q(i_business__is_active=False)).count())
        response['my_saved_offer'] = format_number(models.SavedOffers.objects.filter(i_user=instance, i_business__is_active=True, i_content__is_active=True, i_content__i_sub_category__is_active=True).exclude(Q(i_business__i_user__is_active=False) | Q(i_content__i_brand__is_active=False)).count())
        response['my_friends'] = format_number(models.FriendList.objects.filter(i_user=instance, friends__is_active=True, is_active=True).count())
        response['my_rewards'] = format_number(models.UserReward.objects.filter(i_user=instance).count())
        try:
            response['i_city'] = instance.i_city.name if request.user.lang_code == 1 else instance.i_city.name_ar
            response['i_country'] = instance.i_country.name if request.user.lang_code == 1 else instance.i_country.name_ar
        except Exception:
            response['i_city'] = instance.i_city.name if request.headers.get('Accept-Language') == str(1) else instance.i_city.name_ar
            response['i_country'] = instance.i_country.name if request.headers.get('Accept-Language') == str(1) else instance.i_country.name_ar
        notification_setting_obj = models.NotificationSettings.objects.filter(i_user=instance)
        if notification_setting_obj.exists():
            notification_setting_obj = notification_setting_obj[0]
        else:
            notification_setting_obj = models.NotificationSettings.objects.create(i_user=instance)

        response['notification_settings'] = NotificationSettingsSerializer(notification_setting_obj).data
        response['is_friend'] = False
        user_obj = self.context.get("user_obj")
        if user_obj:
            friends_list = list(models.FriendList.objects.filter(i_user=user_obj).values_list("friends",flat=True))
            if instance.id in friends_list:
                response['is_friend'] = True
                
        return response


class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    type = serializers.IntegerField(required=True)

    def validate(self, data):
        user = models.UserProfile.objects.filter(email=data['email']).exists()
        if user:
            user = models.UserProfile.objects.get(email=data['email'])
            if user.is_type == data['type']:
                if user.check_password(data['password']):
                    if user.is_active and user.is_verified:
                        return super(EmailLoginSerializer, self).validate(data)
                    elif user.is_active == False and user.is_verified:
                        raise serializers.ValidationError(
                            {"email": "You're temporary Blocked by Admin"})
                    else:
                        code_dict = global_methods.generate_otp_tokens()
                        models.OtpToken.objects.filter(i_user=user).delete()
                        models.OtpToken.objects.create(
                            i_user=user, code=code_dict['email_code'], medium="2")
                        email_address = user.email
                        subject = 'OTP for hubur'
                        html_message = "Code has been resend to you. Your otp verification code is %s " % code_dict[
                            'email_code']
                        notifications.sendEmailToSingleUser(
                            html_message, email_address, subject)
                        raise serializers.ValidationError(
                            {"email": "Please Verfy your account. OTP has been send to you."})
                else:
                    raise serializers.ValidationError(
                        {"password": "Incorrect Password"})
            else:
                if user.is_type == 1:
                    raise serializers.ValidationError({"is_type": "Cannot login because your account is Signup with Normal"})
                else:
                    raise serializers.ValidationError({"is_type": "Cannot login because your account is Signup with Social"})
        else:
            raise serializers.ValidationError("No user Exist !")


class ContactLoginSerializer(serializers.Serializer):
    contact = serializers.CharField()
    country_code = serializers.CharField()
    password = serializers.CharField()
    type = serializers.IntegerField(required=True)

    def validate(self, data):
        if '+' in data['country_code']:
            data['country_code'] = data['country_code'].replace("+", "")
        user = models.UserProfile.objects.filter(
            contact=data['contact'], country_code=data['country_code']).exists()
        if user:
            user = models.UserProfile.objects.get(
                contact=data['contact'], country_code=data['country_code'])
            if user.is_type == data['type']:
                if user.check_password(data['password']):
                    if user.is_active and user.is_verified:
                        return super(ContactLoginSerializer, self).validate(data)
                    else:
                        code_dict = global_methods.generate_otp_tokens()
                        models.OtpToken.objects.filter(i_user=user).delete()
                        models.OtpToken.objects.create(
                            i_user=user, code=code_dict['email_code'], medium="2")
                        email_address = user.email
                        subject = 'OTP for hubur'
                        html_message = "Code has been resend to you. Your otp verification code is %s " % code_dict[
                            'email_code']
                        notifications.sendEmailToSingleUser(
                            html_message, email_address, subject)
                        raise serializers.ValidationError(
                            {"contact": "Please Verfy your account. OTP has been send to you."})
                else:
                    raise serializers.ValidationError(
                        {"password": "Incorrect Password"})
            
            else:
                if user.is_type == 1:
                    raise serializers.ValidationError({"is_type": "Cannot login because your account is Signup with Normal"})
                else:
                    raise serializers.ValidationError({"is_type": "Cannot login because your account is Signup with Social"})
        else:
            raise serializers.ValidationError({"contact": "No user Exist !"})


class VerifyUserSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4)
    email = serializers.EmailField(required=False)
    sms = serializers.IntegerField(required=False)
    country_code = serializers.CharField(required=False)

    def create(self, validated_data):
        if 'email' in validated_data:
            query = Q(
                medium="2", code=validated_data['code'], i_user__email=validated_data['email'])
            verify_query = Q(email=validated_data['email'])
        elif 'sms' in validated_data:
            query = Q(medium="1", code=validated_data['code'], i_user__contact=validated_data['sms'],
                      i_user__country_code=validated_data['country_code'])
            verify_query = Q(contact=validated_data['sms'], country_code=str(
                validated_data['country_code']))

        else:
            return {'status': 'Failed to verify'}

        if models.OtpToken.objects.filter(query).exists():

            otp_obj = models.OtpToken.objects.get(query)
            cr_time = otp_obj.created_at
            t2 = cr_time + timedelta(minutes=2)
            now = datetime.now(timezone.utc)
            if now > t2:
                return {'status': 'expired'}
            else:
                if models.UserProfile.objects.filter(verify_query).exists():
                    user = models.UserProfile.objects.filter(
                        verify_query).first()
                    user.is_active = True
                    user.is_verified = True
                    user.save()

                    data_dict = {'status': 'verified'}
                    data_dict['user'] = user

                    return data_dict
                else:
                    return {'status': 'Failed to verify'}
        else:
            return {'status': 'Failed to verify'}

    def validate(self, value):
        if len(value['code']) > 4 or len(value['code']) < 4:
            raise serializers.ValidationError('please enter 4 digit number')
        else:
            if 'email' in value:
                if not (models.UserProfile.objects.filter(email=value['email']).exists()):
                    raise serializers.ValidationError('No email found')
                return value
            elif 'sms' in value:
                if not (models.UserProfile.objects.filter(contact=value['sms']).exists()):
                    raise serializers.ValidationError('No Contact found')
                return value
            else:
                raise serializers.ValidationError('No Medium found')


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = self.context.get("user")
        user.set_password(validated_data['new_password'])
        user.save()
        return user

    def validate(self, data):
        user = self.context.get("user")
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('password')

        errors = dict()
        try:
            if user.check_password(old_password):
                if new_password == confirm_password:
                    validators.validate_password(
                        password=new_password, user=user)
                else:
                    errors['password'] = "Passwords are not matched"
            else:
                errors['password'] = "Old password is not correct"

        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)
        return super(ResetPasswordSerializer, self).validate(data)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    sms = serializers.IntegerField(required=False)
    country_code = serializers.CharField(required=False)
    medium = serializers.CharField(max_length=1)

    def create(self, validated_data):
        code_dict = global_methods.generate_otp_tokens()
        if validated_data.get('medium') == "2":
            user = models.UserProfile.objects.get(
                email=validated_data['email'])
            models.OtpToken.objects.filter(i_user=user).delete()

            otp_obj = models.OtpToken.objects.create(
                i_user=user, code=code_dict['email_code'], medium="2")
            email_address = validated_data['email']
            subject = 'OTP for hubur'
            html_message = "Your otp verification code is %s " % code_dict['email_code']
            notifications.sendEmailToSingleUser(
                html_message, email_address, subject)
        else:
            user = models.UserProfile.objects.get(
                contact=validated_data['sms'], country_code=validated_data['country_code'])
            models.OtpToken.objects.filter(i_user=user).delete()
            otp_obj = models.OtpToken.objects.create(
                i_user=user, code=code_dict['sms_code'], medium="1")
            
            sms_message = "Your otp verification code is %s " % code_dict['sms_code']
            contact_no = "+"+str(validated_data['country_code'])+str(validated_data['sms'])
            notifications.sendMessageToSingleUser(sms_message,contact_no)

        return otp_obj

    def validate(self, value):
        if value['medium'] == "2" and "email" in value:
            if not (models.UserProfile.objects.filter(email=value['email']).exists()):
                raise serializers.ValidationError('No email found')
            elif models.UserProfile.objects.filter(email=value['email'],is_type=2):
                raise serializers.ValidationError('Your Profile is social and password can not be changed.')
            else:
                return value
        elif value['medium'] == "1" and "country_code" in value and "sms" in value:
            if '+' in value['country_code']:
                value['country_code'] = str(value['country_code']).replace("+","")
            if not (models.UserProfile.objects.filter(contact=value['sms'], country_code=value['country_code']).exists()):
                raise serializers.ValidationError('No Contact found')
            elif models.UserProfile.objects.filter(contact=value['sms'], country_code=value['country_code'], is_type=2):
                raise serializers.ValidationError('Your Profile is social and password can not be changed.')
            else:
                return value
        else:
            raise serializers.ValidationError('No Medium found or medium is not correct')


class ResendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    sms = serializers.IntegerField(required=False)
    country_code = serializers.CharField(required=False)
    medium = serializers.CharField(max_length=1)

    def create(self, validated_data):
        code_dict = global_methods.generate_otp_tokens()
        if validated_data.get('medium') == "2":
            user = models.UserProfile.objects.get(
                email=validated_data['email'])
            models.OtpToken.objects.filter(i_user=user).delete()

            otp_obj = models.OtpToken.objects.create(
                i_user=user, code=code_dict['email_code'], medium="2")
            email_address = validated_data['email']
            subject = 'OTP for hubur'
            html_message = "Code has been resend to you. Your otp verification code is %s " % code_dict[
                'email_code']
            notifications.sendEmailToSingleUser(
                html_message, email_address, subject)
        else:
            user = models.UserProfile.objects.get(
                contact=validated_data['sms'], country_code=validated_data['country_code'])
            models.OtpToken.objects.filter(i_user=user).delete()
            otp_obj = models.OtpToken.objects.create(
                i_user=user, code=code_dict['sms_code'], medium="1")
            
            sms_message = "Your otp verification code is %s " % code_dict['sms_code']
            contact_no = "+"+str(validated_data['country_code'])+str(validated_data['sms'])
            notifications.sendMessageToSingleUser(sms_message,contact_no)

        return otp_obj

    def validate(self, value):
        if value['medium'] == "2" and "email" in value:
            if not (models.UserProfile.objects.filter(email=value['email']).exists()):
                raise serializers.ValidationError('No email found')
            return value
        elif value['medium'] == "1" and "country_code" in value and "sms" in value:
            if '+' in value['country_code']:
                value['country_code'] = str(value['country_code']).replace("+","")
            if not (models.UserProfile.objects.filter(contact=value['sms'], country_code=value['country_code']).exists()):
                raise serializers.ValidationError('No Contact found')
            return value
        else:
            raise serializers.ValidationError('No Medium found or medium is not correct')


class ChangePassAfterVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    sms = serializers.IntegerField(required=False)
    country_code = serializers.CharField(required=False)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    code = serializers.CharField(max_length=4)

    def create(self, validated_data):
        if 'email' in validated_data:
            query = Q(email=validated_data['email'])
            token_query = Q(
                i_user__email=validated_data['email'], code=validated_data['code'], medium='2')
        elif 'sms' in validated_data:
            if '+' in validated_data['country_code']:
                validated_data['country_code'] = str(validated_data['country_code']).replace("+","")
            query = Q(
                contact=validated_data['sms'], country_code=validated_data['country_code'])
            token_query = Q(
                i_user__contact=validated_data['sms'], i_user__country_code=validated_data['country_code'], code=validated_data['code'], medium='1')
        else:
            return {'status': 'Medium is not selected'}

        if models.UserProfile.objects.filter(query).exists():

            otp_obj = models.OtpToken.objects.filter(token_query).first()
            if otp_obj:
                cr_time = otp_obj.created_at
                t2 = cr_time + timedelta(minutes=2)
                now = datetime.now(timezone.utc)
                if now > t2:
                    return {'status': 'expired'}
                else:
                    user = models.UserProfile.objects.get(query)
                    user.set_password(validated_data['new_password'])
                    user.save()

                    return {'status': True}
            else:
                return {'status': "Null"}
        else:
            return {'status': False}

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        errors = dict()
        try:
            if new_password == confirm_password:
                validators.validate_password(password=new_password)
            else:
                errors['password'] = "Passwords are not matched"

        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)
        return super(ChangePassAfterVerifySerializer, self).validate(data)


class CitySerializer(serializers.ModelSerializer):
    country = serializers.CharField(source="i_country.name")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('context')
        super().__init__(*args, **kwargs)
        
        try:
            request = self.context.get('request')
            if request.user.is_authenticated:
                if request.user.lang_code == 1:
                    del self.fields['name_ar']
                else:
                    self.fields['name'] = self.fields['name_ar']

            else:
                if request.headers.get('Accept-Language') == str(1):
                    del self.fields['name_ar']
                else:
                    self.fields['name'] = self.fields['name_ar']

        except Exception as e:
            # print(e)
            pass

    class Meta:
        model = models.City
        fields = ('id', 'name', 'name_ar', 'country',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return {k: v if v is not None else "" for k, v in response.items()}


class CountrySerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('context')
        super().__init__(*args, **kwargs)
        
        try:
            request = self.context.get('request')
            if request.user.is_authenticated:
                if request.user.lang_code == 1:
                    del self.fields['name_ar']
                else:
                    self.fields['name'] = self.fields['name_ar']

            else:
                if request.headers.get('Accept-Language') == str(1):
                    del self.fields['name_ar']
                else:
                    self.fields['name'] = self.fields['name_ar']

        except Exception as e:
            # print(e)
            pass
        
    class Meta:
        model = models.Country
        fields = ('id', 'name', 'name_ar',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return {k: v if v is not None else "" for k, v in response.items()}
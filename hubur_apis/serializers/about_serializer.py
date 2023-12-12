
from hubur_apis import models
from rest_framework import serializers

from hubur_apis.serializers.story_serializer import BusinessLogoSerializer


class AboutUsUsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('context')
        super().__init__(*args, **kwargs)
        
        try:
            request = self.context.get('request')
            if request.user.is_authenticated:
                if request.user.lang_code == 1:
                    del self.fields['about_us_ar']
                else:
                    self.fields['about_us'] = self.fields['about_us_ar']

            else:
                if request.headers.get('Accept-Language') == str(1):
                    del self.fields['about_us_ar']
                else:
                    self.fields['about_us'] = self.fields['about_us_ar']

        except Exception as e:
            # print(e)
            pass

    class Meta:
        model = models.Other
        fields = ("about_us", "about_us_ar")


class OtherSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('context')
        super().__init__(*args, **kwargs)
        
        try:
            request = self.context.get('request')
            if request.user.is_authenticated:
                if request.user.lang_code == 1:
                    del self.fields['terms_condition_ar']
                    del self.fields['privacy_policy_ar']
                    del self.fields['disclaimer_ar']
                else:
                    self.fields['terms_condition'] = self.fields['terms_condition_ar']
                    self.fields['privacy_policy'] = self.fields['privacy_policy_ar']
                    self.fields['disclaimer'] = self.fields['disclaimer_ar']

            else:
                if request.headers.get('Accept-Language') == str(1):
                    del self.fields['terms_condition_ar']
                    del self.fields['privacy_policy_ar']
                    del self.fields['disclaimer_ar']
                else:
                    self.fields['terms_condition'] = self.fields['terms_condition_ar']
                    self.fields['privacy_policy'] = self.fields['privacy_policy_ar']
                    self.fields['disclaimer'] = self.fields['disclaimer_ar']

        except Exception as e:
            # print(e)
            pass

    class Meta:
        model = models.Other
        fields = ("terms_condition", "terms_condition_ar", "privacy_policy", "privacy_policy_ar", "disclaimer",  "disclaimer_ar",)


class GetContactUsUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContactUs
        fields = ("mobile","uan","whatsapp","email",)


class ContactUsSerializer(serializers.Serializer):
    full_name = serializers.CharField(allow_null=False, required=True)
    email = serializers.EmailField(allow_null=False, required=True)
    contact = serializers.CharField(allow_null=False, required=True)
    message = serializers.CharField(allow_null=False, required=True)
    class Meta:
        fields = ("full_name","email","contact","message",)


    
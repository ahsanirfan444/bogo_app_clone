
from hubur_apis import models
from rest_framework import serializers

from hubur_apis.serializers.story_serializer import BusinessLogoSerializer


class AboutUsUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Other
        fields = ("about_us",)


class OtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Other
        fields = ("terms_condition","privacy_policy","disclaimer",)


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


    
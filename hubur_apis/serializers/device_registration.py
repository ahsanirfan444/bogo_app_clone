from push_notifications.models import WebPushDevice
from rest_framework import serializers


class RegisterWebForPushNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = WebPushDevice
        fields = ("browser", "p256dh", "auth", "name", "registration_id", "user",)

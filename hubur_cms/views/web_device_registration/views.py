from rest_framework.views import APIView 

from push_notifications.models import WebPushDevice
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from hubur_apis.serializers.device_registration import RegisterWebForPushNotificationSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class RegisterWebDevice(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):
        sessionExists = request.session.get("registration_id", None)
        if not sessionExists:
            serializer = RegisterWebForPushNotificationSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    temp = serializer.save()
                    request.session["registration_id"] = temp.registration_id
                except Exception:
                    raise 
                return Response(status=status.HTTP_201_CREATED)
            
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)




from rest_framework.views import APIView 

from push_notifications.models import WebPushDevice, GCMDevice
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.contrib.auth.models import update_last_login

class GCMDeviceAuthorizedAPIView(APIView):
    def delete(self, request):
        try:
            instance = GCMDevice.objects.filter(user_id=request.user.id)
            instance.update(active = False, date_created=datetime.now())

            request.user.last_login = None
            request.user.save(update_fields=['last_login'])

            return Response({
                'detail': "Gcm Device Unregistered Successfully",
                'status': status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({
                'detail': "Not Found",
                'status': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.response import Response
from core.defaults import DefualtPaginationClass
from rest_framework.permissions import IsAuthenticated
from hubur_apis import models
from rest_framework import status
from rest_framework.views import APIView

from hubur_apis.serializers.notification_serializer import NotificationSerializer

class GetNotificationAPIView(APIView, DefualtPaginationClass):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        notification_obj = models.Notification.objects.filter(user=request.user).exclude(notification_type=3)
        notification_obj = self.paginate_queryset(notification_obj, self.request)
        serializer = NotificationSerializer(notification_obj, many=True)
        if serializer.is_valid:
            return Response({'error': [], 'error_code': '', 'data': serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            error_list = []
            for e in serializer.errors.values():
                error_list.append(e[0])
            return Response({'error': error_list, 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


class ReadNotificationAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        instance = models.Notification.objects.filter(user=request.user, id=request.data.get('id'))
        instance.update(reviewed=True)
        cust_resp = {
            'detail': 'This notification read successfully',
            'status': status.HTTP_200_OK
        }

        return Response(cust_resp, status=status.HTTP_200_OK)
    
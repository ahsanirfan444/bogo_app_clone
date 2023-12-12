from rest_framework.response import Response
from hubur_apis import models
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import notifications
from hubur_apis.serializers.redemption_serializer import (
    RedemptionSerializer, RedemptionCodeSerializer
    )

class CreateRedemptionCodeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer_class = RedemptionCodeSerializer(data=request.data, context={"user_obj":request.user})
        if serializer_class.is_valid():
            serializer_class.save()
            return Response({'error': [], 'error_code': '', 'data': serializer_class.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            error_list = []
            for e in serializer_class.errors.values():
                error_list.append(e[0])
            return Response({'error': error_list, 'error_code': 'HD404', 'data': {},'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


class RedemptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_obj = request.user
        serializer_class = RedemptionSerializer(data=request.data, context={"user_obj":user_obj})
        if serializer_class.is_valid():
            serializer_class.save()
            response = serializer_class.validated_data
            response['i_user'] = user_obj
            models.Redemption.objects.create(**response)

            title = "Redemption Alert"
            msg ="Code for "+ str(response['i_content'].name) +" is " +str(response['code'])
            title_ar = "تنبيه الاسترداد"
            msg_ar ="رمز ل"+ str(response['i_content'].name_ar) +" يكون " +str(response['code'])

            kwargs = {'i_content':str(response['i_content'].id), 'content_name':str(response['i_content'].name), 'avail_code':str(response['code']),'actions':'avail_offer'}
            notifications.sendNotificationToSingleUser(user_obj.id, msg, msg_ar, title, title_ar, 2, response['i_content'].id, "avail_offer",notification_type=7, activityAndroid="FLUTTER_NOTIFICATION_CLICK", activityIOS="FLUTTER_NOTIFICATION_CLICK",code=str(response['code']) ,**kwargs)
            
            return Response({'error': [], 'error_code': '', 'data': ["Redemption Done"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            error_list = []
            for e in serializer_class.errors.values():
                error_list.append(e[0])
            return Response({'error': error_list, 'error_code': 'HD404', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
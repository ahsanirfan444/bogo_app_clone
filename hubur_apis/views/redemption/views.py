from rest_framework.response import Response
from hubur_apis import models
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
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
            return Response({'error': [], 'error_code': '', 'data': ["Redemption Done"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            error_list = []
            for e in serializer_class.errors.values():
                error_list.append(e[0])
            return Response({'error': error_list, 'error_code': 'HD404', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.response import Response
from rest_framework.views import APIView
from hubur_apis import models
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from hubur_apis.serializers.checkin_serializer import (
    CheckinSerializer, GetCheckinListSerializer
    )
from rest_framework import viewsets
from core.defaults import DefualtPaginationClass


class CheckInAPIView(viewsets.ModelViewSet):

    queryset = models.Checkedin.objects.all()
    pagination_class = DefualtPaginationClass
    serializer_class = CheckinSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer_class = CheckinSerializer(data=request.data, context = {'user_obj':request.user})
        if serializer_class.is_valid():
            serializer_class.save()
            reward_point = models.RewardPoints.objects.filter(type=1)
            if reward_point:
                models.UserReward.objects.create(i_user=request.user, i_business_id=serializer_class.data['i_business'], i_point=reward_point[0])
            return Response({'error': [], 'error_code': '', 'data': ["Sucessfully Check In"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            error_list = []
            for e in serializer_class.errors.values():
                error_list.append(e[0])
            return Response({'error': error_list, 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
    def list(self, request, *args, **kwargs):
        user_obj = request.user

        checkin_obj = models.Checkedin.objects.filter(i_user=user_obj, is_active=True).order_by("-updated_at")
        checkin_obj = self.paginate_queryset(checkin_obj)
        checkin_serializer = GetCheckinListSerializer(checkin_obj,many=True)
        if checkin_serializer:
            return Response({'error': [], 'error_code': '', 'data': checkin_serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': [], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
             

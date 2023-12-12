from rest_framework.response import Response
from core.defaults import DefualtPaginationClass
from hubur_apis import models
from rest_framework import status
from hubur_apis.serializers.campaign_serializer import CampaignListSerializer

from rest_framework.views import APIView

class CampaignAPIView(APIView):
     def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            campaign_queryset = models.Campaign.objects.filter(is_active=True).order_by("-created_at")

        else:
            campaign_queryset = models.Campaign.objects.filter(is_active=True).order_by("-created_at")
        serializer = CampaignListSerializer(campaign_queryset, context={"request": request}, many=True)

        return Response({'error': [], 'error_code': '', 'data': serializer.data, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
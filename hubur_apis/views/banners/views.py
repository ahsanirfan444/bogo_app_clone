from rest_framework.response import Response
from hubur_apis import models
from rest_framework.views import APIView
from rest_framework import status
from hubur_apis.serializers.banner_serializer import (
    BannerListSerializer
)


class TopbannerView(APIView):
    permission_classes = []
    def get(self, request, *args, **kwargs):
        banner_obj = models.Banner.objects.filter(is_active=True).exclude(sub_catagory_type__in=["IMAGE","SUB_CATAGORY"])
        context = {'request': request}
        banner_serializer = BannerListSerializer(banner_obj, context= context,many=True)
        return Response({'error': [], 'error_code': 'HD404', 'data': banner_serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
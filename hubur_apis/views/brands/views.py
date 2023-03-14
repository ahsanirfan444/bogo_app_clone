
from rest_framework.response import Response
from hubur_apis import models
from rest_framework.views import APIView
from rest_framework import status
from hubur_apis.serializers.brand_serializer import (
    BrandListSerializer
)

class BrandListAPI(APIView):
    permission_classes = []
    def get(self, request, *args, **kwargs):
        brands_obj = models.Brand.objects.filter(is_active=True)
        context = {'request': request}
        brand_serializer = BrandListSerializer(brands_obj, context= context,many=True)
        return Response({'error': '', 'error_code': 'HD404', 'data': brand_serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)

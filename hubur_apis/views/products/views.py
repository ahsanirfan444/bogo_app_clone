from hubur_apis import models
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from hubur_apis.serializers.products_serializer import (
    GetProductsSerializer
    )


class ProductsAPIView(viewsets.ModelViewSet):

    serializer_class = GetProductsSerializer
    queryset = models.Content.objects.filter(is_active=True)
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name', '^i_sub_category__name']

    def create(self, request, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
       
    def perform_update(self, serializer):
       return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, pk=None):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


    def list(self,request):
        query = self.get_queryset()
        filter_queryset = self.filter_queryset(query)
        serializer = GetProductsSerializer(filter_queryset, many=True)
        if serializer.data:
            return Response({'error': '', 'error_code': '', 'data': serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': '', 'error_code': '', 'data': "No Product Found",'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
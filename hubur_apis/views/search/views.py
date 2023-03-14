from hubur_apis import models
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from hubur_apis.serializers.search_serializer import (
    GetProductsSerializer, GetBusinessSerializer, GetSubCategorySerializer, GetBrandSerializer, PopularSearchSerializer,PopularSearchListSerializer,
    )


class SearchProductAPIView(viewsets.ModelViewSet):

    serializer_class = GetProductsSerializer
    queryset = models.Content.objects.filter(is_active=True)
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']

    def list(self,request):
        
        business_query = models.Business.objects.filter(is_active=True)
        business_filter_queryset = self.filter_queryset(business_query)
        business_serializer = GetBusinessSerializer(business_filter_queryset, many=True)

        product_query = models.Content.objects.filter(is_active=True)
        product_filter_queryset = self.filter_queryset(product_query)
        product_serializer = GetProductsSerializer(product_filter_queryset, many=True)

        brand_query = models.Brand.objects.filter(is_active=True)
        brand_filter_queryset = self.filter_queryset(brand_query)
        brand_serializer = GetBrandSerializer(brand_filter_queryset, many=True)

        sub_category_query = models.SubCategories.objects.filter(is_active=True)
        sub_category_filter_queryset = self.filter_queryset(sub_category_query)
        sub_category_serializer = GetSubCategorySerializer(sub_category_filter_queryset, many=True)

        product_list = product_serializer.data
        business_list =business_serializer.data
        brand_list =brand_serializer.data
        sub_category_list =sub_category_serializer.data
        

        data_dict = product_list + business_list + brand_list + sub_category_list
        if data_dict:
            for data in data_dict:
                if 'picture' in data:
                    popular_search_serializer = PopularSearchSerializer(data={"name":data['name'],"url":data['picture']})
                elif 'logo_pic' in data:
                    popular_search_serializer = PopularSearchSerializer(data={"name":data['name'],"url":data['logo_pic']})
                elif 'image' in data:
                    popular_search_serializer = PopularSearchSerializer(data={"name":data['name'],"url":data['image']})
                else:
                    popular_search_serializer = PopularSearchSerializer(data={"name":data['name']})
                if popular_search_serializer.is_valid():
                    if 'count' not in popular_search_serializer.validated_data:
                        popular_search_serializer.save()
                else:
                    return Response({'error':popular_search_serializer.errors , 'error_code': '', 'data': "",'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': '', 'error_code': '', 'data': data_dict,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': '', 'error_code': '', 'data': "No Result Found",'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        
    def create(self, request, *args, **kwargs):
        return status.HTTP_405_METHOD_NOT_ALLOWED

    def update(self, request, pk, *args, **kwargs):
        return status.HTTP_405_METHOD_NOT_ALLOWED
       
    def perform_update(self, serializer):
       return status.HTTP_405_METHOD_NOT_ALLOWED

    def retrieve(self, request, pk=None):
        return status.HTTP_405_METHOD_NOT_ALLOWED

    def partial_update(self, request, pk=None):
        return status.HTTP_405_METHOD_NOT_ALLOWED


class PopularSearchAPIView(viewsets.ModelViewSet):

    serializer_class = PopularSearchListSerializer
    queryset = models.PopularSearch.objects.filter(is_active=True).order_by('-count')[:5]
    def list(self,request):

        query = self.get_queryset()
        filter_queryset = self.filter_queryset(query)
        serializer = PopularSearchListSerializer(filter_queryset, many=True)
        if serializer:
            return Response({'error': '', 'error_code': '', 'data': serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': '', 'error_code': '', 'data': "No Popular Search Found",'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        
    def create(self, request, *args, **kwargs):
        return status.HTTP_405_METHOD_NOT_ALLOWED

    def update(self, request, pk, *args, **kwargs):
        return status.HTTP_405_METHOD_NOT_ALLOWED
       
    def perform_update(self, serializer):
       return status.HTTP_405_METHOD_NOT_ALLOWED

    def retrieve(self, request, pk=None):
        return status.HTTP_405_METHOD_NOT_ALLOWED

    def partial_update(self, request, pk=None):
        return status.HTTP_405_METHOD_NOT_ALLOWED


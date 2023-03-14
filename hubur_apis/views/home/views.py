from rest_framework.response import Response
from hubur_apis import models
from rest_framework import status
from rest_framework import viewsets
from hubur_apis.serializers.search_serializer import (
    PopularSearchListSerializer,
    )

from hubur_apis.serializers.brand_serializer import (
    BrandListSerializer,
)

from hubur_apis.serializers.banner_serializer import (
    BannerListSerializer,HomeBusinessSerializer
)

class HomeAPIView(viewsets.ModelViewSet):

    serializer_class = PopularSearchListSerializer
    queryset = models.PopularSearch.objects.filter(is_active=True).order_by('-count')[:5]

    def list(self,request):
        all_data_dict = dict()
        query = self.get_queryset()
        filter_queryset = self.filter_queryset(query)
        popular_search_serializer = PopularSearchListSerializer(filter_queryset, many=True)
        popular_search = popular_search_serializer.data
        all_data_dict['popular_search'] = popular_search

        brands_obj = models.Brand.objects.filter(is_active=True)
        context = {'request': request}
        brand_serializer = BrandListSerializer(brands_obj, context= context,many=True)
        all_data_dict['brands'] = brand_serializer.data


        banner_obj = models.Banner.objects.filter(is_active=True, i_subcatagory=None)
        context = {'request': request}
        banner_serializer = BannerListSerializer(banner_obj, context= context,many=True)
        all_data_dict['banner'] = banner_serializer.data

        query_sub_category = models.Banner.objects.filter(is_active=True, sub_catagory_type="SUB_CATAGORY").exclude(i_subcatagory=None)
        if query_sub_category:
            query_sub_category = query_sub_category.first()
            
            if request.user.username:
                catagories_obj = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
                print(catagories_obj)
                business_obj = models.Business.objects.filter(i_subcategory=query_sub_category.i_subcatagory, i_category__in=catagories_obj)
            else:
                business_obj = models.Business.objects.filter(i_subcategory=query_sub_category.i_subcatagory)
            
            after_have_you_been_serializer = HomeBusinessSerializer(business_obj, context= context,many=True)
            if after_have_you_been_serializer:
                all_data_dict['after_have_you_been'] = after_have_you_been_serializer.data
            else:
                all_data_dict['after_have_you_been'] = []
        else:
            all_data_dict['after_have_you_been'] = []

        query_image = models.Banner.objects.filter(is_active=True, sub_catagory_type="IMAGE").exclude(i_subcatagory=None)
        if query_image:
            query_image = query_image.first()

            if request.user.username:
                catagories_obj = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
                business_obj = models.Business.objects.filter(i_subcategory=query_image.i_subcatagory, i_category__in=catagories_obj)
            else:
                business_obj = models.Business.objects.filter(i_subcategory=query_image.i_subcatagory)
            
            before_my_favorites_serializer = HomeBusinessSerializer(business_obj, context= context,many=True)
            if before_my_favorites_serializer:
                all_data_dict['before_my_favorites'] = before_my_favorites_serializer.data
            else:
                all_data_dict['before_my_favorites'] = []
        else:
            all_data_dict['before_my_favorites'] = []

        
        if all_data_dict:
            return Response({'error': [], 'error_code': '', 'data': [all_data_dict],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': [], 'error_code': '', 'data': ["No Data Found"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)

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
from core.defaults import DefualtPaginationClass
from hubur_apis import models
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from django.core.paginator import Paginator, PageNotAnInteger
from hubur_apis.serializers.brand_serializer import BrandListSerializer
from hubur_apis.serializers.home_serializer import HomeBusinessSerializer
from django.db.models import Q
from hubur_apis.serializers.search_serializer import (
    GetProductsSerializer, GetBusinessSerializer, GetSubCategorySerializer, GetBrandSerializer, PopularSearchSerializer,PopularSearchListSerializer, SearchSerializer,
    )


class SearchProductAPIView(viewsets.ModelViewSet):

    serializer_class = GetProductsSerializer
    queryset = models.Content.objects.filter(is_active=True)
    filter_backends = [filters.SearchFilter]
    pagination_class = DefualtPaginationClass
    search_fields = ['^name']

    def list(self,request):
            # brand_list = []
            # if 'sub_id' in request.GET:
            #     sub_catagories_list = list(models.SubCategories.objects.filter(is_active=True).values_list('id',flat=True))
            #     sub_id = request.GET['sub_id']
            #     if int(sub_id) in sub_catagories_list:
            #         if request.user.username:
            #             user_cat_list = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
            #             content_query_filtered = models.Content.objects.filter(is_active=True, i_sub_category__id=sub_id, i_business__i_category__in=user_cat_list)
            #             business_query_filtered = models.Business.objects.filter(is_active=True, i_subcategory__id=sub_id, i_category__in=user_cat_list)
            #         else:
            #             content_query_filtered = models.Content.objects.filter(is_active=True, i_sub_category__id=sub_id)
            #             business_query_filtered = models.Business.objects.filter(is_active=True, i_subcategory__id=sub_id)
            #     else:
            #         return Response({'error': ["No Result Found"], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            # else:
            #     if request.user.username:
            #         user_cat_list = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
            #         content_query_filtered = models.Content.objects.filter(is_active=True, i_business__i_category__in=user_cat_list)
            #         business_query_filtered = models.Business.objects.filter(is_active=True, i_category__in=user_cat_list)
            #     else:
            #         business_query_filtered = models.Business.objects.filter(is_active=True)
            #         content_query_filtered = models.Content.objects.filter(is_active=True)
                
            # if 'i_subcategory__name' in self.search_fields:
            #     self.search_fields.remove('^i_subcategory__name')

            # brand_query = models.Brand.objects.filter(is_active=True)
            # brand_paginate_queryset = self.paginate_queryset(brand_query)
            # if brand_paginate_queryset:
            #     brand_filter_queryset = self.filter_queryset(brand_paginate_queryset)
            #     brand_serializer = GetBrandSerializer(brand_filter_queryset, many=True)
            #     brand_list = brand_serializer.data
            # else:
            #     brand_list = []
                    
            # self.search_fields.append('^i_sub_category__name')
            # product_query = content_query_filtered
            # product_paginate_queryset = self.paginate_queryset(product_query)
            # if product_paginate_queryset:
            #     product_filter_queryset = self.filter_queryset(product_paginate_queryset)
            #     product_serializer = GetProductsSerializer(product_filter_queryset, many=True)
            #     product_list = product_serializer.data
            # else:
            #     product_list = []

            # self.search_fields.remove('^i_sub_category__name')

            # self.search_fields.append('^i_subcategory__name')
            # business_query = business_query_filtered
            # business_paginate_queryset = self.paginate_queryset(business_query)
            # business_filter_queryset = self.filter_queryset(business_paginate_queryset)
            # business_serializer = GetBusinessSerializer(business_filter_queryset, many=True)
            # if business_serializer:
            #     business_list = business_serializer.data
            # else:
            #     business_list = []
            # self.search_fields.remove('^i_subcategory__name')

            # data_dict = product_list + business_list + brand_list
            # paginated_data = self.paginate_queryset(data_dict)
            # if paginated_data:
            #         return Response({'error': [], 'error_code': '', 'data': paginated_data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            # else:
            #     return Response({'error': ["No Result Found"], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        try:
            product_page_not_found = brand_page_not_found = business_page_not_found = False
            count = 10
            brand_list = []
            if 'sub_id' in request.GET:
                sub_catagories_list = list(models.SubCategories.objects.filter(is_active=True).values_list('id',flat=True))
                sub_id = request.GET['sub_id']
                if int(sub_id) in sub_catagories_list:
                    if request.user.username:
                        user_cat_list = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
                        content_query_filtered = models.Content.objects.filter(is_active=True, i_sub_category__id=sub_id, i_business__i_category__in=user_cat_list)
                        business_query_filtered = models.Business.objects.filter(is_active=True, i_subcategory__id=sub_id, i_category__in=user_cat_list, i_category__is_active=True)
                    else:
                        content_query_filtered = models.Content.objects.filter(is_active=True, i_sub_category__id=sub_id)
                        business_query_filtered = models.Business.objects.filter(is_active=True, i_subcategory__id=sub_id)
                else:
                    return Response({'error': ["No Result Found"], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                if request.user.username:
                    user_cat_list = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
                    content_query_filtered = models.Content.objects.filter(is_active=True, i_business__i_category__in=user_cat_list, i_category__is_active=True)
                    business_query_filtered = models.Business.objects.filter(is_active=True, i_category__in=user_cat_list)
                else:
                    business_query_filtered = models.Business.objects.filter(is_active=True)
                    content_query_filtered = models.Content.objects.filter(is_active=True)
                    
                brand_query = models.Brand.objects.filter(is_active=True)
                brand_filter_queryset = self.filter_queryset(brand_query)
                if brand_filter_queryset:

                    paginator = Paginator(brand_filter_queryset,count-7)
                    page = request.GET.get('page')
                    try:
                        brand_filter_queryset = paginator.page(page)
                    except PageNotAnInteger:
                        brand_filter_queryset = paginator.page(1)
                    except:
                        brand_filter_queryset = []
                        brand_page_not_found = True

                    brand_serializer = GetBrandSerializer(brand_filter_queryset, many=True)
                    brand_list =brand_serializer.data
                    count -= len(brand_list)
                else:
                    brand_filter_queryset = []
                    
            self.search_fields.append('^i_sub_category__name')
            product_query = content_query_filtered
            product_filter_queryset = self.filter_queryset(product_query)
            if product_filter_queryset:
                paginator = Paginator(product_filter_queryset, count-4)
                page = request.GET.get('page')
                try:
                    product_filter_queryset = paginator.page(page)
                except PageNotAnInteger:
                    product_filter_queryset = paginator.page(1)
                except:
                    product_filter_queryset = []
                    product_page_not_found = True


                product_serializer = GetProductsSerializer(product_filter_queryset, many=True)
                product_list = product_serializer.data
                count -= len(product_list)
            else:
                product_list = []

            self.search_fields.remove('^i_sub_category__name')

            self.search_fields.append('^i_subcategory__name')
            business_query = business_query_filtered
            business_filter_queryset = self.filter_queryset(business_query)
            if business_filter_queryset:

                paginator = Paginator(business_filter_queryset, count)
                page = request.GET.get('page')
                try:
                    business_filter_queryset = paginator.page(page)
                except PageNotAnInteger:
                    business_filter_queryset = paginator.page(1)
                except:
                    business_filter_queryset = []
                    business_page_not_found = True
            else:
                business_filter_queryset = []

            business_serializer = GetBusinessSerializer(business_filter_queryset, many=True)
            self.search_fields.remove('^i_subcategory__name')

            if all([product_page_not_found,brand_page_not_found,business_page_not_found]):
                return Response({"detail": "Invalid page."}, status=status.HTTP_404_NOT_FOUND)
            


            business_list =business_serializer.data

    

            data_dict = product_list + business_list + brand_list
            if len(product_list) == 0:
                product_list = True
            if len(business_list) == 0:
                business_list = True
            if len(brand_list) == 0:
                brand_list = True
            if data_dict:
                return Response({'error': [], 'error_code': '', 'data': data_dict,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                if all([product_list,business_list,brand_list]) and any([product_page_not_found,brand_page_not_found,business_page_not_found]):
                    return Response({"detail": "Invalid page."}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({'error': ["No result found"], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except Exception as error:
                error_list = []
                for e in repr(error):
                    error_list.append(e[0])
                return Response({'error': [repr(error)], 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            
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


class PopularSearchAPIView(viewsets.ModelViewSet):

    serializer_class = PopularSearchListSerializer
    queryset = models.PopularSearch.objects.filter(is_active=True).order_by('-count')[:5]
    def list(self,request):

        if request.user.username:
            user_cat_list = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category__name',flat=True))
            query2 = models.PopularSearch.objects.filter(is_active=True, catagory__in=user_cat_list)
            query1 = models.PopularSearch.objects.filter(is_active=True).exclude(type="Business")
            query = query1.union(query2).order_by('-count')[:5]

        else:
            query = self.get_queryset()
        filter_queryset = self.filter_queryset(query)
        serializer = PopularSearchListSerializer(filter_queryset, many=True)
        if serializer:
            return Response({'error': [], 'error_code': '', 'data': serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': ["No Popular Search Found"], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        
    def create(self, request, *args, **kwargs):

        if 'id' in request.data and 'type' in request.data:
            id = request.data['id']
            search_type = request.data['type']
            if search_type == 'Business':
                try:
                    business_obj = models.Business.objects.get(id=id)

                    business_serializer = HomeBusinessSerializer(business_obj)
                    business_obj = business_serializer.data
                    data_dict = {"name":business_obj['name'], "url":business_obj['logo_pic'], "type_id":business_obj['id'], "type":search_type ,"catagory":business_obj['catagory']}
                    popular_search_serializer = PopularSearchSerializer(data=data_dict)

                    if popular_search_serializer.is_valid():
                        if 'count' not in popular_search_serializer.validated_data:
                            popular_search_serializer.save()
                    return Response({'error': [], 'error_code': '', 'data': popular_search_serializer.data,'status':status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
                except :
                    return Response({'error': ["No Business found"], 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

            elif search_type == 'Brand':
                try:
                    brand_obj = models.Brand.objects.get(id=id)
                    brand_serializer = BrandListSerializer(brand_obj)
                    brand_obj = brand_serializer.data
                    data_dict = {"name":brand_obj['name'], "url":brand_obj['image'], "type_id":brand_obj['id'], "type":search_type}
                    popular_search_serializer = PopularSearchSerializer(data=data_dict)
                    if popular_search_serializer.is_valid():
                        if 'count' not in popular_search_serializer.validated_data:
                            popular_search_serializer.save()
                    return Response({'error': [], 'error_code': '', 'data': popular_search_serializer.validated_data,'status':status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
                except :
                    return Response({'error': ["No Brand found"], 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': ["No Result found"], 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        else:
            if 'id' not in request.data and 'type' not in request.data:
                error = "type and id are missing"
            elif 'id' not in request.data:
                error = "id is missing"
            else:
                error = "type is missing"

            return Response({'error': [error], 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
       
    def perform_update(self, serializer):
       return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, pk=None):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class SubCatagoriesView(viewsets.ModelViewSet):

    serializer_class = GetSubCategorySerializer
    queryset = models.SubCategories.objects.filter(is_active=True)
    def list(self,request):
        if request.user.username:
            user_cat_list = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
            sub_catagories_query = models.SubCategories.objects.filter(is_active=True, i_category_id__in=user_cat_list, i_category__is_active=True)
        else:
            sub_catagories_query = models.SubCategories.objects.filter(is_active=True ,i_category__is_active=True)
        sub_catagories_filter_queryset = self.filter_queryset(sub_catagories_query)
        if sub_catagories_filter_queryset:
            serializer = GetSubCategorySerializer(sub_catagories_filter_queryset, many=True)
            if serializer:
                return Response({'error': [], 'error_code': '', 'data': serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        return Response({'error': ['No Result Found'], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        
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


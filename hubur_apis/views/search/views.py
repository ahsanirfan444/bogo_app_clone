from django.shortcuts import get_object_or_404
from core.defaults import DefualtPaginationClass
from hubur_apis import models
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from django.core.paginator import Paginator, PageNotAnInteger
from django.db.models import Q
from hubur_apis.serializers.home_serializer import HomeBusinessWithAddressSerializer
from hubur_apis.serializers.search_serializer import (
    GetProductsSerializer, GetBusinessSerializer, GetSubCategorySerializer, GetBrandSerializer, PopularSearchSerializer,PopularSearchListSerializer, SubCatagoryBannerSerializer,
    )
from random import sample,random,shuffle
from django.db.models import Case, When

from hubur_apis.serializers.trending_discount_serializer import (
    TrendingDiscountForCatagoriesSerializer,
    )

class SearchProductAPIView(viewsets.ModelViewSet):

    serializer_class = GetProductsSerializer
    queryset = models.Content.objects.filter(is_active=True)
    filter_backends = [filters.SearchFilter]
    pagination_class = DefualtPaginationClass
    search_fields = ['^name','name']

    def list(self,request):
        # try:
            product_page_not_found = brand_page_not_found = business_page_not_found = False
            count = 10
            brand_list = []
            if 'sub_id' in request.GET:
                sub_catagories_list = list(models.SubCategories.objects.filter(is_active=True).values_list('id',flat=True))
                sub_id = request.GET['sub_id']
                if int(sub_id) in sub_catagories_list:
                    content_query_filtered = models.Content.objects.filter(is_active=True, i_sub_category__id=sub_id)
                    business_query_filtered = models.Business.objects.filter(is_active=True, i_subcategory__id=sub_id)
                else:
                    return Response({'error': ["No Result Found"], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
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


            else:
                product_filter_queryset = []

            product_serializer = GetProductsSerializer(product_filter_queryset, many=True)
            product_list = product_serializer.data
            count -= len(product_list)
            

            self.search_fields.append('^i_subcategory__name')
            business_query = business_query_filtered
            business_filter_queryset = self.filter_queryset(business_query)
            self.search_fields.remove('^i_subcategory__name')
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
        # except Exception as error:
        #         error_list = []
        #         for e in repr(error):
        #             error_list.append(e[0])
        #         return Response({'error': [repr(error)], 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            
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
            user_cat_list = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category__id',flat=True))
            query2 = models.PopularSearch.objects.filter(is_active=True, i_business__i_category__in=user_cat_list)
            query1 = models.PopularSearch.objects.filter(is_active=True).exclude(type="Business")
            query = (query1 | query2)[:5]

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
                    input_dict = {"type":search_type,"obj_id":id}
                    popular_search_serializer = PopularSearchSerializer(data=input_dict)

                    if popular_search_serializer.is_valid():
                        serialized_data = popular_search_serializer.validated_data
                        if 'count' not in serialized_data:
                            serialized_data['i_business_id'] = serialized_data['obj_id']
                            del serialized_data['obj_id']
                            
                            models.PopularSearch.objects.create(**serialized_data)

                    return Response({'error': [], 'error_code': '', 'data': serialized_data,'status':status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
                except Exception as e:
                    print(repr(e))
                    return Response({'error': ["No Business found"], 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

            elif search_type == 'Brand':
                try:
                    input_dict = {"type":search_type,"obj_id":id}
                    popular_search_serializer = PopularSearchSerializer(data=input_dict)
                    if popular_search_serializer.is_valid():
                        serialized_data = popular_search_serializer.validated_data
                        if 'count' not in serialized_data:
                            serialized_data['i_brand_id'] = serialized_data['obj_id']
                            del serialized_data['obj_id']
                            
                            models.PopularSearch.objects.create(**serialized_data)

                    return Response({'error': [], 'error_code': '', 'data': popular_search_serializer.validated_data,'status':status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
                except :
                    return Response({'error': ["No Brand found"], 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            
            elif search_type == 'Content':
                try:
                    input_dict = {"type":search_type,"obj_id":id}
                    popular_search_serializer = PopularSearchSerializer(data=input_dict)
                    if popular_search_serializer.is_valid():
                        serialized_data = popular_search_serializer.validated_data
                        if 'count' not in serialized_data:
                            serialized_data['i_content_id'] = serialized_data['obj_id']
                            del serialized_data['obj_id']
                            
                            models.PopularSearch.objects.create(**serialized_data)

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


class SearchForSubCatagoriesView(viewsets.ModelViewSet):

    serializer_class = GetBusinessSerializer
    queryset = models.SubCategories.objects.filter(is_active=True)
    filter_backends = [filters.SearchFilter]
    pagination_class = DefualtPaginationClass
    search_fields = ['^name','name','i_subcategory__name']

    def list(self,request):
        try:
            page = self.request.query_params.get('page')
            search = self.request.query_params.get('search')
            sub_id = self.request.query_params.get('sub_id')
            td_id = self.request.query_params.get('td_id')


            sub_catagories_query = models.SubCategories.objects.filter(is_active=True ,i_category__is_active=True)
            sub_cat_list_for_filter = True
            sub_catagories_serializer = GetSubCategorySerializer(sub_catagories_query,context={'sub_cat_list_for_filter':sub_cat_list_for_filter}, many=True)
            

            sub_catagories_banner = models.Banner.objects.filter(is_active=True, position=5)
            sub_catagories_banner_serializer = SubCatagoryBannerSerializer(sub_catagories_banner, many=True)

            all_trending_discount = models.TrendingDiscount.objects.filter(is_active=True).order_by('name')
            all_trending_discount_serializer = TrendingDiscountForCatagoriesSerializer(all_trending_discount, many=True)
            
            if request.user.username:
                user_checkin_cat_list = list(set(models.Checkedin.objects.filter(i_user=request.user).values_list('i_business__i_category__id',flat=True)))
                business_id_list = list(models.Business.objects.filter(is_active=True, i_category__in=user_checkin_cat_list).values_list('id',flat=True))

                you_may_like_ids = sample(business_id_list,len(business_id_list))[:5]
                you_may_like = models.Business.objects.filter(id__in=you_may_like_ids)
                ordering = {id: index for index, id in enumerate(you_may_like_ids)}

                you_may_like = you_may_like.annotate(
                    order=Case(
                        *[When(id=id, then=index) for id, index in ordering.items()],
                        default=len(ordering)
                    )
                ).order_by('order')
            else:
                you_may_like = []
            you_may_like_serializer = self.get_serializer(you_may_like, many=True)
                

            filter_key_error = []
            if sub_id or td_id:
                sub_obj = None
                if sub_id:
                    try:
                        sub_obj = models.SubCategories.objects.get(is_active=True, i_category__is_active=True, id =int(sub_id))
                        business_filter_queryset = models.Business.objects.filter(is_active=True, i_subcategory__id=sub_obj.id).order_by("name")
                    except:
                        filter_key_error.append("No sub catagory found")
                    
                if td_id:

                    try:
                        if sub_obj:
                            query = Q(is_active=True, i_subcategory__id=sub_obj.id)
                        else:
                            query = Q(is_active=True)
                        trending_discount_list = models.TrendingDiscount.objects.get(is_active=True, id =int(td_id))
                        business_filter_queryset = trending_discount_list.i_business.filter(query).order_by("name")
                    except:
                        filter_key_error.append("No trending discount found")
                        
                if filter_key_error:
                    return Response({'error': [], 'sub_cat':sub_catagories_serializer.data ,
                                            'trending_discount':all_trending_discount_serializer.data,'banner':sub_catagories_banner_serializer.data ,
                                            'data': filter_key_error,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)

                business_filter_queryset = self.filter_queryset(business_filter_queryset)
                paginator = Paginator(business_filter_queryset,10)
                try:
                    business_filter_queryset = paginator.page(page)
                    
                except PageNotAnInteger:
                    business_filter_queryset = paginator.page(1)
                except:
                    return Response({'error': [], 'sub_cat':sub_catagories_serializer.data ,
                                            'trending_discount':all_trending_discount_serializer.data,'banner':sub_catagories_banner_serializer.data ,
                                            'data': {"detail": "Invalid page."},'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
                
                business_filter_queryset = (self.get_serializer(business_filter_queryset, many=True)).data
                if business_filter_queryset:
                    return Response({'error': [], 'sub_cat':sub_catagories_serializer.data ,
                                            'trending_discount':all_trending_discount_serializer.data, 'you_may_like':you_may_like_serializer.data, 'banner':sub_catagories_banner_serializer.data ,
                                            'data': business_filter_queryset,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': [], 'sub_cat':sub_catagories_serializer.data ,
                                            'trending_discount':all_trending_discount_serializer.data, 'you_may_like':you_may_like_serializer.data, 'banner':sub_catagories_banner_serializer.data ,
                                            'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)

            else:                
                
                if page == '1' and (search == None or not search):

                    if request.user.username:
                        user_checkin_sub_list = list(set(models.Checkedin.objects.filter(i_user=request.user).values_list('i_business__i_subcategory__id',flat=True)))
                        if user_checkin_sub_list:
                            query = Q(is_active=True, i_subcategory__in=user_checkin_sub_list)
                        else:
                            query = Q(is_active=True)

                        business_id_list = list(models.Business.objects.filter(query).values_list('id',flat=True))
                    else:    
                        business_id_list = list(models.Business.objects.filter(is_active=True).values_list('id',flat=True))

                    all_random_business_ids = sample(business_id_list,len(business_id_list))[:10]
                    all_random_business = models.Business.objects.filter(id__in=all_random_business_ids)
                    ordering = {id: index for index, id in enumerate(all_random_business_ids)}

                    all_random_business = all_random_business.annotate(
                        order=Case(
                            *[When(id=id, then=index) for id, index in ordering.items()],
                            default=len(ordering)
                        )
                    ).order_by('order')


                    self.request.session['random_businesses'] = all_random_business_ids
                    business_filter_queryset = self.get_serializer(all_random_business, many=True)

                elif page == '1' and search:
                    business_filter_queryset = models.Business.objects.filter(is_active=True).order_by("-created_at")
                    business_filter_queryset = self.filter_queryset(business_filter_queryset)
                    paginator = Paginator(business_filter_queryset,10)
                    try:
                        business_filter_queryset = paginator.page(int(page))
                    except:
                        return Response({'error': [], 'sub_cat':sub_catagories_serializer.data ,
                                            'trending_discount':all_trending_discount_serializer.data,'banner':sub_catagories_banner_serializer.data ,
                                            'data': {"detail": "Invalid page."},'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
                    
                    business_filter_queryset = self.get_serializer(business_filter_queryset, many=True)
                    
                else:
                    random_businesses = self.request.session.get('random_businesses', [])
                    business_filter_queryset = models.Business.objects.filter(is_active=True).exclude(pk__in=random_businesses).order_by("-created_at")
                    business_filter_queryset = self.filter_queryset(business_filter_queryset)

                    paginator = Paginator(business_filter_queryset,10)
                    try:
                        business_filter_queryset = paginator.page(int(page)-1)
                    except:
                        return Response({'error': [], 'sub_cat':sub_catagories_serializer.data ,
                                            'trending_discount':all_trending_discount_serializer.data,'banner':sub_catagories_banner_serializer.data ,
                                            'data': {"detail": "Invalid page."},'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)

                    business_filter_queryset = self.get_serializer(business_filter_queryset, many=True)

                                    
            business_list = business_filter_queryset.data

            if business_list:
                return Response({'error': [],'sub_cat':sub_catagories_serializer.data, 'you_may_like':you_may_like_serializer.data, 'trending_discount':all_trending_discount_serializer.data,'banner':sub_catagories_banner_serializer.data , 'data': business_list,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': ["No result found"],'sub_cat':sub_catagories_serializer.data, 'you_may_like':you_may_like_serializer.data, 'trending_discount':all_trending_discount_serializer.data,'banner':sub_catagories_banner_serializer.data  , 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'error': [repr(error)], 'sub_cat':[] ,'trending_discount':[],'banner': [], 'data': [], 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
    def retrieve(self, request, pk=None):
        return Response({'error': ['Method is not allowed'], 'sub_cat':[] ,'trending_discount':[],'banner': [], 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'sub_cat':[] ,'trending_discount':[],'banner': [], 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'sub_cat':[] ,'trending_discount':[],'banner': [], 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
       
    def perform_update(self, serializer):
       return Response({'error': ['Method is not allowed'], 'sub_cat':[] ,'trending_discount':[],'banner': [], 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response({'error': ['Method is not allowed'], 'sub_cat':[] ,'trending_discount':[],'banner': [], 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
from rest_framework.response import Response
from core.defaults import DefualtPaginationClass
from global_methods import distance
from hubur_apis import models
from rest_framework import status
from rest_framework import viewsets
from datetime import timedelta
from django.utils import timezone
from hubur_apis.serializers.home_serializer import (
    HomeBusinessSerializer,
    HomeBusinessWithAddressSerializer,
    LocationForGuestModeSerializer,
    NearByDealsSerializer,
    )
from hubur_apis.serializers.search_serializer import (
    GetSubCategorySerializer,
    PopularSearchListSerializer,
    )

from hubur_apis.serializers.brand_serializer import (
    HomeBrandListSerializer,
)

from hubur_apis.serializers.banner_serializer import (
    BannerListSerializer
)
from hubur_apis.serializers.trending_discount_serializer import TrendingDiscountSerializer

class HomeAPIView(viewsets.ModelViewSet):

    pagination_class = DefualtPaginationClass
    serializer_class = PopularSearchListSerializer
    queryset = models.PopularSearch.objects.filter(is_active=True).order_by('-count')[:5]

    def list(self,request):
        all_data_dict = dict()

        trending_discount_list = models.TrendingDiscount.objects.filter(is_active=True).order_by("-created_at")[:5]
        trending_discount_serializer = TrendingDiscountSerializer(trending_discount_list, many=True)
        if trending_discount_serializer:
            all_data_dict['trending_discount'] = trending_discount_serializer.data
        else:
            all_data_dict['trending_discount'] = []

        
        if request.user.username:
            user_cat_list = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category__name',flat=True))
            query2 = models.PopularSearch.objects.filter(is_active=True, catagory__in=user_cat_list)
            query1 = models.PopularSearch.objects.filter(is_active=True).exclude(type="Business")
            query = query1.union(query2).order_by('-count')[:5]
        else:
            query = self.get_queryset()

        filter_queryset = self.filter_queryset(query)
        popular_search_serializer = PopularSearchListSerializer(filter_queryset, many=True)
        popular_search = popular_search_serializer.data
        all_data_dict['popular_search'] = popular_search

        brands_obj = models.Brand.objects.filter(is_active=True).order_by('-created_at')[:10]
        context = {'request': request}
        brand_serializer = HomeBrandListSerializer(brands_obj, context= context,many=True)
        all_data_dict['brands'] = brand_serializer.data


        banner_obj = models.Banner.objects.filter(is_active=True, i_subcatagory=None)
        context = {'request': request}
        banner_serializer = BannerListSerializer(banner_obj, context= context,many=True)
        all_data_dict['banner'] = banner_serializer.data
        
        
        
        if request.user.username:
            catagories_obj = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
            business_obj = models.Business.objects.filter(is_active=True, i_category__in=catagories_obj).order_by('-created_at')
            user_long = request.user.long
            user_lat = request.user.lat
            if 'long' and 'lat' in request.data:
                location_serializer = LocationForGuestModeSerializer(data=request.data)
                if location_serializer.is_valid():
                    user_long = location_serializer.data['long']
                    user_lat = location_serializer.data['lat']
                    updates = {'long': user_long, 'lat': user_lat}
                    models.UserProfile.objects.filter(id=request.user.id).update(**updates)
                else:
                    all_data_dict['near_by_deals'] = "please enable your location"

            if user_long and user_lat:
                business_obj_list = []
                context = {'user_long': user_long,'user_lat':user_lat}
                for business in business_obj:
                    total_distance = distance(user_long,user_lat,business.long,business.lat)
                    if float(total_distance) <= 10:
                        business_obj_list.append(business)
                    if len(business_obj_list) == 4:
                        break

                business_serializer = HomeBusinessWithAddressSerializer(business_obj_list, context= context,many=True)
                all_data_dict['near_by_deals'] = business_serializer.data
            else:
                all_data_dict['near_by_deals'] = "please enable your location"
        else:

            business_obj_list = []
            if "lat" and "long" in request.data:

                user_long = request.data['long']
                user_lat = request.data['lat']

                location_serializer = LocationForGuestModeSerializer(data={"lat":user_lat,"long":user_long})
                if location_serializer.is_valid():
                    user_lat = location_serializer.validated_data['lat']
                    user_long = location_serializer.validated_data['long']
                    
                    business_obj = models.Business.objects.filter(is_active=True)
                    for business in business_obj:
                        total_distance = distance(user_long,user_lat,business.long,business.lat)
                        if float(total_distance) <= 10:
                            business_obj_list.append(business)
                        if len(business_obj_list) == 4:
                            break

                    business_serializer = HomeBusinessWithAddressSerializer(business_obj_list, context= context,many=True)
                    all_data_dict['near_by_deals'] = business_serializer.data
                    
                else:
                    error_list = []
                    for error in location_serializer.errors.values():
                        error_list.append(error[0])
                    return Response({'error': error_list, 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            else:
                all_data_dict['near_by_deals'] = "please enable your location"


        query_sub_category = models.Banner.objects.filter(is_active=True, position=3).exclude(i_subcatagory=None)
        if query_sub_category:
            query_sub_category = query_sub_category.first()
            
            if request.user.username:
                catagories_obj = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
                business_obj = models.Business.objects.filter(i_subcategory=query_sub_category.i_subcatagory, i_category__in=catagories_obj).order_by('-created_at')[:4]
            else:
                business_obj = models.Business.objects.filter(i_subcategory=query_sub_category.i_subcatagory).order_by('-created_at')[:4]
            
            after_have_you_been_serializer = HomeBusinessWithAddressSerializer(business_obj, context= context,many=True)
            if after_have_you_been_serializer:
                all_data_dict['after_have_you_been_sub_cat'] = query_sub_category.i_subcatagory.name
                all_data_dict['after_have_you_been'] = after_have_you_been_serializer.data
            else:
                all_data_dict['after_have_you_been_sub_cat'] = ""
                all_data_dict['after_have_you_been'] = []
        else:
            all_data_dict['after_have_you_been_sub_cat'] = ""
            all_data_dict['after_have_you_been'] = []

        query_image = models.Banner.objects.filter(is_active=True, position=4).exclude(i_subcatagory=None)
        if query_image:
            query_image = query_image.first()

            if request.user.username:
                catagories_obj = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
                business_obj = models.Business.objects.filter(i_subcategory=query_image.i_subcatagory, i_category__in=catagories_obj).order_by('-created_at')[:4]
            else:
                business_obj = models.Business.objects.filter(i_subcategory=query_image.i_subcatagory).order_by('-created_at')[:4]
            
            before_my_favorites_serializer = HomeBusinessSerializer(business_obj, context= context,many=True)
            if before_my_favorites_serializer:
                all_data_dict['before_my_favorites_sub_cat'] = query_image.i_subcatagory.name
                all_data_dict['before_my_favorites'] = before_my_favorites_serializer.data
            else:
                all_data_dict['before_my_favorites_sub_cat'] = ""
                all_data_dict['before_my_favorites'] = []
        else:
            all_data_dict['before_my_favorites_sub_cat'] = ""
            all_data_dict['before_my_favorites'] = []

        if request.user.username:
            last_week = timezone.now().date() - timedelta(days=7)
            last_check_in = models.Checkedin.objects.filter(i_user=request.user, created_at__date__gte=last_week).order_by("-created_at").first()
            if last_check_in and last_check_in.i_business.is_active:
                user_cat_list = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
                business_list = list(models.Business.objects.filter(is_active=True, i_category_id__in=user_cat_list).order_by('-created_at'))

                user_long = request.user.long
                user_lat = request.user.lat

                if 'long' and 'lat' in request.data:
                    location_serializer = LocationForGuestModeSerializer(data=request.data)
                    if location_serializer.is_valid():
                        user_long = location_serializer.data['long']
                        user_lat = location_serializer.data['lat']
                        updates = {'long': user_long, 'lat': user_lat}
                        models.UserProfile.objects.filter(id=request.user.id).update(**updates)
                    else:
                        all_data_dict['have_you_been_there'] = "please enable your location"

                all_business_data = []

                for business in business_list:
                    total_distance = distance(user_long,user_lat,business.long,business.lat)
                    if float(total_distance) <= 10:
                        all_business_data.append(business)
                        if len(all_business_data) == 4:
                            break

                serializer = HomeBusinessSerializer(all_business_data, many=True)
                serializer_data = serializer.data
                serializer_data = filter(None, serializer_data)
                if serializer_data:
                    all_data_dict['have_you_been_there'] = serializer_data
                else:
                    all_data_dict['have_you_been_there'] = []
            else:
                all_data_dict['have_you_been_there'] = []
        else:
            business_list = list(models.Business.objects.filter(is_active=True).order_by('-created_at')[:4])
            serializer = HomeBusinessSerializer(business_list, many=True)
            serializer_data = serializer.data
            serializer_data = filter(None, serializer_data)
            if serializer_data:
                all_data_dict['have_you_been_there'] = serializer_data


        if request.user.username:
            user_cat_list = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
            sub_catagories_query = models.SubCategories.objects.filter(is_active=True, i_category_id__in=user_cat_list, i_category__is_active=True)
        else:
            sub_catagories_query = models.SubCategories.objects.filter(is_active=True ,i_category__is_active=True)
        if sub_catagories_query:
            serializer = GetSubCategorySerializer(sub_catagories_query, many=True)
            all_data_dict['all_sub_catagories'] = serializer.data
        else:
            all_data_dict['all_sub_catagories'] = []
        
        if all_data_dict:
            return Response({'error': [], 'error_code': '', 'data': [all_data_dict],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': [], 'error_code': '', 'data': ["No Data Found"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)

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
    
class AfterHaveYouBeenListAPIView(viewsets.ModelViewSet):

    serializer_class = HomeBusinessWithAddressSerializer
    pagination_class = DefualtPaginationClass
    queryset = models.Business.objects.filter(is_active=True).order_by('-created_at')

    def list(self,request):
        query_sub_category = models.Banner.objects.filter(is_active=True, position=3).exclude(i_subcatagory=None)
        if query_sub_category:
            query_sub_category = query_sub_category.first()
        
            if request.user.username:
                catagories_obj = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
                business_obj = models.Business.objects.filter(is_active=True, i_subcategory=query_sub_category.i_subcatagory, i_category__in=catagories_obj).order_by('-created_at')
            else:
                business_obj = models.Business.objects.filter(is_active=True, i_subcategory=query_sub_category.i_subcatagory).order_by('-created_at')

            context = {'request': request}

            business_obj = self.paginate_queryset(business_obj)
            
            after_have_you_been_serializer = HomeBusinessWithAddressSerializer(business_obj, context= context,many=True)
            if after_have_you_been_serializer:
                return Response({'error': [], 'error_code': '', 'data': after_have_you_been_serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': ['No Data Found'], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': ['No Data Found'], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        
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

class BeforeMyFavListAPIView(viewsets.ModelViewSet):

    serializer_class = HomeBusinessWithAddressSerializer
    pagination_class = DefualtPaginationClass

    queryset = models.Business.objects.filter(is_active=True).order_by('-created_at')

    def list(self,request):
        query_image = models.Banner.objects.filter(is_active=True, position=4).exclude(i_subcatagory=None)
        if query_image:
            query_image = query_image.first()

            if request.user.username:
                catagories_obj = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
                business_obj = models.Business.objects.filter(i_subcategory=query_image.i_subcatagory, i_category__in=catagories_obj).order_by('-created_at')
            else:
                business_obj = models.Business.objects.filter(i_subcategory=query_image.i_subcatagory).order_by('-created_at')
            
            context = {'request': request}

            business_obj = self.paginate_queryset(business_obj)
            
            before_my_favorites_serializer = HomeBusinessWithAddressSerializer(business_obj, context= context,many=True)
            if before_my_favorites_serializer:
                return Response({'error': [], 'error_code': '', 'data': before_my_favorites_serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': ['No Data Found'], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': ['No Data Found'], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
    
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
    


class HaveYouBeenThereListAPIView(viewsets.ModelViewSet):

    serializer_class = HomeBusinessSerializer
    pagination_class = DefualtPaginationClass
    queryset = models.Business.objects.filter(is_active=True).order_by('-created_at')

    def list(self,request):
        query_image = models.Banner.objects.filter(is_active=True, position=4).exclude(i_subcatagory=None)
        if query_image:
            query_image = query_image.first()

            if request.user.username:
                last_week = timezone.now().date() - timedelta(days=7)
                last_check_in = models.Checkedin.objects.filter(i_user=request.user, created_at__date__gte=last_week).order_by("-created_at").first()
                if last_check_in and last_check_in.i_business.is_active:
                    user_cat_list = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
                    business_list = list(models.Business.objects.filter(is_active=True, i_category_id__in=user_cat_list).order_by('-created_at'))
                    all_business_data = []

                    for business in business_list:
                        total_distance = distance(request.user.long,request.user.lat,business.long,business.lat)
                        if float(total_distance) <= 10:
                            all_business_data.append(business)

                    business_list = self.paginate_queryset(all_business_data)
                    serializer = HomeBusinessSerializer(business_list, many=True)
                    
                else:
                    return Response({'error': ['No Data Found'], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                business_list = list(models.Business.objects.filter(is_active=True).order_by('-created_at'))
                business_list = self.paginate_queryset(business_list)
                serializer = HomeBusinessSerializer(business_list, many=True)
            
            
            serializer_data = serializer.data
            serializer_data = filter(None, serializer_data)
            if serializer_data:
                return Response({'error': [], 'error_code': '', 'data': serializer_data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': ['No Data Found'], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
                return Response({'error': ['No Data Found'], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
    
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
    


class DiscoverBrandListAPIView(viewsets.ModelViewSet):

    pagination_class = DefualtPaginationClass
    serializer_class = HomeBusinessSerializer
    queryset = models.Business.objects.filter(is_active=True).order_by('-created_at')

    def list(self,request):
        brands_obj = models.Brand.objects.filter(is_active=True).order_by('-created_at')
        brands_obj = self.paginate_queryset(brands_obj)
       
        context = {'request': request}
        brand_serializer = HomeBrandListSerializer(brands_obj, context= context,many=True)      
        return Response({'error': [], 'error_code': '', 'data': brand_serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
       
    
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
    


class NearByDealsListAPIView(viewsets.ModelViewSet):

    pagination_class = DefualtPaginationClass
    serializer_class = HomeBusinessWithAddressSerializer
    queryset = models.Business.objects.filter(is_active=True).order_by('-created_at')

    def list(self,request):
        if request.user.username:
            catagories_obj = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
            user_long = request.user.long
            user_lat = request.user.lat
            if user_long and user_lat:
                all_business_data = []

                business_objs = models.Business.objects.filter(is_active=True, i_category__in=catagories_obj).order_by('-created_at')
                for business in business_objs:
                    total_distance = distance(user_long,user_lat,business.long,business.lat)
                    if float(total_distance) <= 10:
                        all_business_data.append(business)

                business_obj = self.paginate_queryset(all_business_data)
                context = {'user_long': user_long,'user_lat':user_lat}
            else:
                return Response({'error': ["No result found, please enable your location"], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            location_serializer = LocationForGuestModeSerializer(data=request.data)
            if location_serializer.is_valid():
                user_lat = location_serializer.validated_data['lat']
                user_long = location_serializer.validated_data['long']

                all_business_data = []

                business_objs = models.Business.objects.filter(is_active=True).order_by('-created_at')
                for business in business_objs:
                    total_distance = distance(user_long,user_lat,business.long,business.lat)
                    if float(total_distance) <= 10:
                        all_business_data.append(business)

                business_obj = self.paginate_queryset(all_business_data)
                context = {'user_long': user_long,'user_lat':user_lat}
            else:
                error_list = []
                for error in location_serializer.errors.values():
                    error_list.append(error[0])
                return Response({'error': error_list, 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        
        business_serializer = NearByDealsSerializer(business_obj, context= context,many=True)

        return Response({'error': [], 'error_code': '', 'data': business_serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
    

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
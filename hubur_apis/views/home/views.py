from rest_framework.response import Response
from core.defaults import DefualtPaginationClass
from global_methods import distance, format_number, localized_subcategory_name
from hubur_apis import models
from rest_framework import status
from rest_framework import viewsets
from datetime import timedelta, datetime
from django.utils import timezone
from django.db.models import Q,When,Case
from rest_framework.views import APIView
from hubur_apis.serializers.content_serializer import (
    ContentDetailSerializer,
    )
from hubur_apis.serializers.home_serializer import (
    HomeBusinessSerializer, HomeBusinessWithAddressSerializer, LocationForGuestModeSerializer, NearByDealsSerializer,
    )
from hubur_apis.serializers.offer_serializer import (
    OfferDetailSerializer,
    )
from hubur_apis.serializers.search_serializer import (
    GetSubCategorySerializer,PopularSearchListSerializer,
    )
from hubur_apis.serializers.brand_serializer import (
    HomeBrandListSerializer,
)

from hubur_apis.serializers.banner_serializer import (
    BannerListSerializer,
)
from hubur_apis.serializers.trending_discount_serializer import (
    TrendingDiscountSerializer,
    )
from push_notifications.models import WebPushDevice, GCMDevice

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from concurrent.futures import ThreadPoolExecutor

class HomeAPIView(viewsets.ModelViewSet):

    pagination_class = DefualtPaginationClass
    serializer_class = PopularSearchListSerializer
    queryset = models.PopularSearch.objects.filter(is_active=True).order_by('-count')[:5]


    def list(self,request):
        max_workers = 10
        all_data_dict = dict()

        total_time_now = datetime.now()
        time_now = datetime.now()
       
        trending_discount_list = models.TrendingDiscount.objects.filter(is_active=True).order_by("-created_at")[:12]
        trending_discount_serializer = TrendingDiscountSerializer(trending_discount_list, context={'request': request}, many=True)
        if trending_discount_serializer:
            all_data_dict['trending_discount'] = trending_discount_serializer.data
        else:
            all_data_dict['trending_discount'] = []

        time_then = datetime.now()
        milliseconds = (time_then-time_now).microseconds/1000
        # print(milliseconds,"trending_discount................")


        time_now = datetime.now()
        if request.user.username:
            user_cat_list = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category__id',flat=True))
            popular_search_query = models.PopularSearch.objects
            query2 = popular_search_query.filter(is_active=True, i_business__i_category__in=user_cat_list).exclude(Q(i_business__i_user__is_active=False) | Q(i_business__is_active=False) | Q(i_content__is_active=False) | Q(i_content__i_brand__is_active=False) | Q(i_content__i_business__is_active=False) | Q(i_content__i_business__i_user__is_active=False) | Q(type="Brand"))
            query1 = popular_search_query.filter(is_active=True).exclude(Q(type="Business") | Q(type="Content") | Q(i_brand__is_active=False))
            query = (query1 | query2)[:5]

        else:
            popular_search_query = models.PopularSearch.objects.filter(is_active=True)
            query2 = popular_search_query.exclude(Q(i_business__i_user__is_active=False) | Q(i_business__is_active=False) | Q(i_content__is_active=False) | Q(i_content__i_brand__is_active=False) | Q(i_content__i_business__is_active=False) | Q(i_content__i_business__i_user__is_active=False) | Q(type="Brand"))
            query1 = popular_search_query.exclude(Q(type="Business") | Q(type="Content") | Q(i_brand__is_active=False))
            query = (query1 | query2)[:5]
        filter_queryset = self.filter_queryset(query)
        popular_search_serializer = PopularSearchListSerializer(filter_queryset, context={"request": request}, many=True)
        popular_search = popular_search_serializer.data
        all_data_dict['popular_search'] = popular_search

        time_then = datetime.now()
        milliseconds = (time_then-time_now).microseconds/1000
        # print(milliseconds,"popular_search................")
        time_now = datetime.now()

        brands_obj = models.Brand.objects.filter(is_active=True).order_by('-created_at')[:10]
        context = {'request': request}
        brand_serializer = HomeBrandListSerializer(brands_obj, context= context,many=True)
        all_data_dict['brands'] = brand_serializer.data

        time_then = datetime.now()
        milliseconds = (time_then-time_now).microseconds/1000
        # print(milliseconds,"brands................")
        time_now = datetime.now()


        banner_obj = models.Banner.objects.filter(is_active=True).exclude(position=5)
        banner_obj = banner_obj.filter(language=request.user.lang_code) if request.user.is_authenticated else banner_obj.filter(language=request.headers.get('Accept-Language'))
        context = {'request': request}
        banner_serializer = BannerListSerializer(banner_obj, context= context,many=True)
        all_data_dict['banner'] = banner_serializer.data

        time_then = datetime.now()
        milliseconds = (time_then-time_now).microseconds/1000
        # print(milliseconds,"banner................")
        time_now = datetime.now()
        
        
        
        if request.user.username:
            catagories_obj = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
            business_obj = models.Business.objects.filter(is_active=True, i_category__in=catagories_obj).exclude(i_user__is_active=False).order_by('-is_featured')
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
                context = {'user_long': user_long,'user_lat':user_lat, "request": request}
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
                    
                    business_obj = models.Business.objects.filter(is_active=True).exclude(i_user__is_active=False).order_by('-is_featured')
                    for business in business_obj:
                        total_distance = distance(user_long,user_lat,business.long,business.lat)
                        if float(total_distance) <= 10:
                            business_obj_list.append(business)
                        if len(business_obj_list) == 4:
                            break
                    def business_serializer_def(business):
                        return business
                    
                    with ThreadPoolExecutor(max_workers=max_workers) as executor:
                        executor.map(business_serializer_def, business_obj_list)
                    business_serializer = HomeBusinessWithAddressSerializer(business_obj_list, context= context,many=True)
                    all_data_dict['near_by_deals'] = business_serializer.data
                    
                else:
                    error_list = []
                    for error in location_serializer.errors.values():
                        error_list.append(error[0])
                    return Response({'error': error_list, 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            else:
                all_data_dict['near_by_deals'] = "please enable your location"
            
        time_then = datetime.now()
        milliseconds = (time_then-time_now).microseconds/1000
        # print(milliseconds,"near_by_deals................")
        time_now = datetime.now()


        query_sub_category = models.Banner.objects.filter(is_active=True, position=3, i_subcatagory__is_active=True).exclude(i_subcatagory=None)
        if query_sub_category:
            query_sub_category = query_sub_category.first()
            
            if request.user.username:
                catagories_obj = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
                business_obj = models.Business.objects.filter(is_active=True, i_subcategory=query_sub_category.i_subcatagory, i_category__in=catagories_obj).exclude(i_user__is_active=False).order_by('-is_featured')[:4]
            else:
                business_obj = models.Business.objects.filter(is_active=True, i_subcategory=query_sub_category.i_subcatagory).exclude(i_user__is_active=False).order_by('-is_featured')[:4]
            
            after_have_you_been_serializer = HomeBusinessWithAddressSerializer(business_obj, context= context,many=True)
            if after_have_you_been_serializer:
                all_data_dict['after_have_you_been_sub_cat'] = localized_subcategory_name(request, query_sub_category)
                all_data_dict['after_have_you_been'] = after_have_you_been_serializer.data
            else:
                all_data_dict['after_have_you_been_sub_cat'] = ""
                all_data_dict['after_have_you_been'] = []
        else:
            all_data_dict['after_have_you_been_sub_cat'] = ""
            all_data_dict['after_have_you_been'] = []

        time_then = datetime.now()
        milliseconds = (time_then-time_now).microseconds/1000
        # print(milliseconds,"after_have_you_been................")
        time_now = datetime.now()

        query_image = models.Banner.objects.filter(is_active=True, position=4, i_subcatagory__is_active=True).exclude(i_subcatagory=None)
        if query_image:
            query_image = query_image.first()

            if request.user.username:
                catagories_obj = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
                business_obj = models.Business.objects.filter(is_active=True,  i_subcategory=query_image.i_subcatagory, i_category__in=catagories_obj).exclude(i_user__is_active=False).order_by('-is_featured')[:4]
            else:
                business_obj = models.Business.objects.filter(is_active=True, i_subcategory=query_image.i_subcatagory).exclude(i_user__is_active=False).order_by('-is_featured')[:4]
            
            before_my_favorites_serializer = HomeBusinessSerializer(business_obj, context= context,many=True)
            if before_my_favorites_serializer:
                all_data_dict['before_my_favorites_sub_cat'] = localized_subcategory_name(request, query_image)
                all_data_dict['before_my_favorites'] = before_my_favorites_serializer.data
            else:
                all_data_dict['before_my_favorites_sub_cat'] = ""
                all_data_dict['before_my_favorites'] = []
        else:
            all_data_dict['before_my_favorites_sub_cat'] = ""
            all_data_dict['before_my_favorites'] = []
        
        time_then = datetime.now()
        milliseconds = (time_then-time_now).microseconds/1000
        # print(milliseconds,"before_my_favorites................")
        time_now = datetime.now()
        
        if request.user.username:
            all_business_list = list(models.MyFavourite.objects.filter(i_user=request.user).values_list("i_business",flat=True).order_by('-created_at'))[:4]
            all_business_dict = {id_val: pos for pos, id_val in enumerate(all_business_list)}
            whens = [When(id=id_val, then=pos) for id_val, pos in all_business_dict.items()]
            order_by = Case(*whens)

            all_business = models.Business.objects.filter(id__in=all_business_list, is_active=True).exclude(i_user__is_active=False).order_by(order_by)
            context = {'request': request}
            my_favourite_serializer = HomeBusinessWithAddressSerializer(all_business, context= context ,many=True)
            if my_favourite_serializer:
                all_data_dict['my_favorites'] = my_favourite_serializer.data
            else:
                all_data_dict['my_favorites'] = []
        else:
            all_data_dict['my_favorites'] = []
        
        time_then = datetime.now()
        milliseconds = (time_then-time_now).microseconds/1000
        # print(milliseconds,"my_favorites................")
        time_now = datetime.now()

        

        if request.user.username:
            last_week = timezone.now().date() - timedelta(days=7)
            last_check_in = models.Checkedin.objects.filter(i_user=request.user, created_at__date__gte=last_week, i_business__is_active=True, is_active=True).order_by("-created_at").first()
            if last_check_in:
                last_check_in_long = last_check_in.i_business.long
                last_check_in_lat = last_check_in.i_business.lat
                user_cat_list = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
                business_list = list(models.Business.objects.filter(is_active=True, i_category_id__in=user_cat_list).exclude(i_user__is_active=False).order_by('-is_featured'))

                all_business_data = []

                for business in business_list:
                    total_distance = distance(business.long,business.lat,last_check_in_long,last_check_in_lat)
                    if total_distance == 0:
                        continue
                    if float(total_distance) <= 10:
                        all_business_data.append(business)
                        if len(all_business_data) == 4:
                            break

                serializer = HomeBusinessSerializer(all_business_data, context={"request": request}, many=True)
                serializer_data = serializer.data
                serializer_data = filter(None, serializer_data)
                if serializer_data:
                    all_data_dict['have_you_been_there'] = serializer_data
                else:
                    all_data_dict['have_you_been_there'] = []
            else:
                all_data_dict['have_you_been_there'] = []
        else:
            business_list = list(models.Business.objects.filter(is_active=True).exclude(i_user__is_active=False).order_by('-is_featured')[:4])
            serializer = HomeBusinessSerializer(business_list, context={"request": request}, many=True)
            serializer_data = serializer.data
            serializer_data = filter(None, serializer_data)
            if serializer_data:
                all_data_dict['have_you_been_there'] = serializer_data
            
        time_then = datetime.now()
        milliseconds = (time_then-time_now).microseconds/1000
        # print(milliseconds,"have_you_been_there................")
        time_now = datetime.now()

        if request.user.username:
            catagories_obj = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
            business_ids = list(models.Business.objects.filter(i_category__in=catagories_obj, is_claimed=2, is_active=True).exclude(i_user__is_active=False).values_list('id',flat=True))
        else:
            business_ids = list(models.Business.objects.filter(is_claimed=2, is_active=True).exclude(i_user__is_active=False).values_list('id',flat=True))
        
        
        hot_offers_time_now = datetime.now()

        all_offers = models.Offers.objects.filter(is_active=True, is_expiry=False, i_business__in=business_ids).order_by('-is_featured')
        hot_offer_list = list(all_offers.filter(type=4)[:6].values_list("i_content",flat=True))
        
        hot_content_list = models.Content.objects.filter(id__in=hot_offer_list, is_active=True, i_sub_category__is_active=True, i_business__is_active=True).exclude(Q(i_brand__is_active=False) | Q(i_business__i_user__is_active=False))[:6]
        def hot_serializer(hot):
            return hot
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(hot_serializer, hot_content_list)

        if request.user.username:
            user_obj = request.user
        else:
            user_obj = None

        hot_offer_content = ContentDetailSerializer(hot_content_list, context={'user_obj':user_obj, "request": request}, many=True)
        hot_offers = hot_offer_content.data
        hot_offers.sort(key=lambda item: item["is_featured"], reverse=True)

        hot_offers_time_then = datetime.now()
        milliseconds = (hot_offers_time_then-hot_offers_time_now).microseconds/1000
        # print(milliseconds,"hot_offers_time_now................")
        daily_offers_time_now = datetime.now()



        
     

        daily_offer_list = list(all_offers.filter(type=1)[:6].values_list("i_content",flat=True))
        

        daily_content_list = models.Content.objects.filter(id__in=daily_offer_list, is_active=True, i_business__is_active=True, i_sub_category__is_active=True).exclude(Q(i_brand__is_active=False) | Q(i_business__i_user__is_active=False))[:6]
        

        def daily_serializer(daily):
            return daily
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(daily_serializer, daily_content_list)
            
        daily_offer_content = ContentDetailSerializer(daily_content_list, context={'user_obj':user_obj, "request": request}, many=True)
        daily_offers = daily_offer_content.data
        daily_offers.sort(key=lambda item: item["is_featured"], reverse=True)

        daily_offers_time_then = datetime.now()
        milliseconds = (daily_offers_time_then-daily_offers_time_now).microseconds/1000
        # print(milliseconds,"daily_offers_time_then................")
        weekly_offers_time_now = datetime.now()
       

        weekly_offer_list = list(all_offers.filter(type=2)[:6].values_list("i_content",flat=True))

        weekly_content_list = models.Content.objects.filter(id__in=weekly_offer_list, is_active=True, i_sub_category__is_active=True, i_business__is_active=True).exclude(Q(i_brand__is_active=False) | Q(i_business__i_user__is_active=False))[:6]
        
        def weekly_serializer(weekly):
            return weekly
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(weekly_serializer, weekly_content_list)
        
        weekly_offer_content = ContentDetailSerializer(weekly_content_list, context={'user_obj':user_obj, "request": request}, many=True)
        weekly_offers = weekly_offer_content.data
        weekly_offers.sort(key=lambda item: item["is_featured"], reverse=True)

        weekly_offers_time_then = datetime.now()
        milliseconds = (weekly_offers_time_then-weekly_offers_time_now).microseconds/1000
        # print(milliseconds,"weekly_offers_time_now................")
        monthly_offers_time_now = datetime.now()

        monthly_offer_list = list(all_offers.filter(type=3)[:6].values_list("i_content",flat=True))

        monthly_content_list = models.Content.objects.filter(id__in=monthly_offer_list, is_active=True, i_sub_category__is_active=True, i_business__is_active=True).exclude(Q(i_brand__is_active=False) | Q(i_business__i_user__is_active=False))
        
        def monthly_serializer(monthly):
            return monthly
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(monthly_serializer, monthly_content_list)

        monthly_offer_content = ContentDetailSerializer(monthly_content_list, context={'user_obj':user_obj, "request": request}, many=True)
        monthly_offers = monthly_offer_content.data
        monthly_offers.sort(key=lambda item: item["is_featured"], reverse=True)

        monthly_offers_time_then = datetime.now()
        milliseconds = (monthly_offers_time_then-monthly_offers_time_now).microseconds/1000
        # print(milliseconds,"monthly_offers_time_then................")




        all_data_dict['offers']= [hot_offers, daily_offers, weekly_offers, monthly_offers]

        time_then = datetime.now()
        milliseconds = (time_then-time_now).microseconds/1000
        # print(milliseconds,"offers................")
        time_now = datetime.now()


        sub_catagories_query = models.SubCategories.objects.filter(is_active=True ,i_category__is_active=True)
        if sub_catagories_query:
            serializer = GetSubCategorySerializer(sub_catagories_query, context={"request": request}, many=True)
            all_data_dict['all_sub_catagories'] = serializer.data
        else:
            all_data_dict['all_sub_catagories'] = []
        if request.user.username:
            channel_ids = list(set(models.Message.objects.filter(receiver=request.user).values_list("channel_id",flat=True)))

            all_data_dict['message_count'] = models.Chat.objects.filter(channel_id__in=channel_ids, is_read=False, count__gt=0).count()
            all_data_dict['notification_count'] = models.Notification.objects.filter(user=request.user,is_read=False).exclude(notification_type=3).count()
        else:    
            all_data_dict['message_count'] = 0
            all_data_dict['notification_count'] = 0

        time_then = datetime.now()
        milliseconds = (time_then-time_now).microseconds/1000
        # print(milliseconds,"message_count................")
        time_now = datetime.now()

        if request.user.is_authenticated:
            # update and remove gcm devices
            gcm = GCMDevice.objects.filter(~Q(user_id=request.user.id) & Q(active=False))
            gcm.update(active=False)
                
            gcm = GCMDevice.objects.filter(user=request.user, active=False)
            gcm.delete()

        
        time_then = datetime.now()
        milliseconds = (time_then-time_now).microseconds/1000
        # print(milliseconds,"GCMDevice................")


        total_time_then = datetime.now()
        milliseconds = (total_time_then-total_time_now).microseconds/1000
        # print(milliseconds,"Total................")
        
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
    queryset = models.Business.objects.filter(is_active=True).exclude(i_user__is_active=False).order_by('-created_at')

    def list(self,request):
        query_sub_category = models.Banner.objects.filter(is_active=True, position=3).exclude(i_subcatagory=None)
        if query_sub_category:
            query_sub_category = query_sub_category.first()
        
            if request.user.username:
                catagories_obj = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
                business_obj = models.Business.objects.filter(is_active=True, i_subcategory=query_sub_category.i_subcatagory, i_category__in=catagories_obj).exclude(i_user__is_active=False).order_by('-is_featured')
            else:
                business_obj = models.Business.objects.filter(is_active=True, i_subcategory=query_sub_category.i_subcatagory).exclude(i_user__is_active=False).order_by('-is_featured')

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

    queryset = models.Business.objects.filter(is_active=True).exclude(i_user__is_active=False).order_by('-created_at')

    def list(self,request):
        query_image = models.Banner.objects.filter(is_active=True, position=4).exclude(i_subcatagory=None)
        if query_image:
            query_image = query_image.last()

            if request.user.username:
                catagories_obj = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
                business_obj = models.Business.objects.filter(is_active=True, i_subcategory=query_image.i_subcatagory, i_category__in=catagories_obj).exclude(i_user__is_active=False).order_by('-is_featured')
            else:
                business_obj = models.Business.objects.filter(is_active=True, i_subcategory=query_image.i_subcatagory).exclude(i_user__is_active=False).order_by('-is_featured')
            
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
    queryset = models.Business.objects.filter(is_active=True).exclude(i_user__is_active=False).order_by('-created_at')

    def list(self,request): 
        if request.user.username:
            last_week = timezone.now().date() - timedelta(days=7)
            last_check_in = models.Checkedin.objects.filter(i_user=request.user, created_at__date__gte=last_week, i_business__is_active=True, is_active=True).order_by("-created_at").first()
            if last_check_in:
                last_check_in_long = last_check_in.i_business.long
                last_check_in_lat = last_check_in.i_business.lat
                user_cat_list = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
                business_list = list(models.Business.objects.filter(is_active=True, i_category_id__in=user_cat_list).exclude(i_user__is_active=False).order_by('-is_featured'))


                all_business_data = []

                for business in business_list:
                    total_distance = distance(business.long,business.lat,last_check_in_long,last_check_in_lat)
                    if total_distance == 0:
                        continue
                    if float(total_distance) <= 10:
                        all_business_data.append(business)

                business_list = self.paginate_queryset(all_business_data)
                serializer = HomeBusinessSerializer(business_list, context={"request": request}, many=True)
                
            else:
                return Response({'error': ['No Data Found'], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            business_list = list(models.Business.objects.filter(is_active=True).exclude(i_user__is_active=False).order_by('-is_featured'))
            business_list = self.paginate_queryset(business_list)
            serializer = HomeBusinessSerializer(business_list, context={"request": request}, many=True)
        
        
        serializer_data = serializer.data
        serializer_data = filter(None, serializer_data)
        if serializer_data:
            return Response({'error': [], 'error_code': '', 'data': serializer_data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
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
    queryset = models.Business.objects.filter(is_active=True).exclude(i_user__is_active=False).order_by('-created_at')

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
    queryset = models.Business.objects.filter(is_active=True, i_user__is_active=True).order_by('-created_at')

    def list(self,request):
        if request.user.username:
            catagories_obj = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
            user_long = request.user.long
            user_lat = request.user.lat
            if user_long and user_lat:
                all_business_data = []

                business_objs = models.Business.objects.filter(is_active=True, i_category__in=catagories_obj).exclude(i_user__is_active=False).order_by('-is_featured')
                for business in business_objs:
                    total_distance = distance(user_long,user_lat,business.long,business.lat)
                    if float(total_distance) <= 10:
                        all_business_data.append(business)

                business_obj = self.paginate_queryset(all_business_data)
                context = {'user_long': user_long,'user_lat':user_lat, "request": request}
            else:
                return Response({'error': ["No result found, please enable your location"], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            user_lat = self.request.query_params.get('lat')
            user_long = self.request.query_params.get('long')
            location_serializer = LocationForGuestModeSerializer(data={"lat":user_lat,"long":user_long})
            if location_serializer.is_valid():
                user_lat = location_serializer.validated_data['lat']
                user_long = location_serializer.validated_data['long']

                all_business_data = []

                business_objs = models.Business.objects.filter(is_active=True).exclude(i_user__is_active=False).order_by('-is_featured')
                for business in business_objs:
                    total_distance = distance(user_long,user_lat,business.long,business.lat)
                    if float(total_distance) <= 10:
                        all_business_data.append(business)

                business_obj = self.paginate_queryset(all_business_data)
                context = {'user_long': user_long,'user_lat':user_lat, "request": request}
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
    
class AllProductsInOfferAPIView(viewsets.ModelViewSet):

    serializer_class = ContentDetailSerializer
    queryset = models.Content.objects.filter(is_active=True)
    pagination_class = DefualtPaginationClass

    def list(self,request):
        try:
            type_param = int(self.request.query_params.get('type'))
        except:
            type_param = ""
        if request.user.username:
            catagories_obj = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
            business_ids = list(models.Business.objects.filter(i_category__in=catagories_obj, is_claimed=2).exclude(i_user__is_active=False).values_list('id',flat=True))
            query = Q(i_business__in=business_ids, is_active=True, is_expiry=False)
        else:
            query = Q(is_active=True, is_expiry=False)
        
        if type_param:
            content_list = models.Content.objects.filter(is_active=True).exclude(Q(i_brand__is_active=False) | Q(i_business__i_user__is_active=False) | Q(i_sub_category__is_active=False) | Q(i_business__is_active=False)).values_list("id",flat=True)
            offers = models.Offers.objects.filter(query,type=type_param, i_content__in=content_list).order_by('-is_featured').distinct()
        else:
            return Response({'error': 'Invalid type', 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            
        if offers:
            offer_serializer = OfferDetailSerializer(offers, context={"request": request}, many=True)
            offer_serializer = offer_serializer.data
            if offer_serializer:
                offer_list = []
                for offer in offer_serializer:
                    offer_list.extend(offer['result'])

            serializer = self.paginate_queryset(offer_list)
            return Response({'error': '', 'error_code': '', 'data': serializer,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': '', 'error_code': '', 'data': ["No Offer found"],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
    def create(self, request, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
       
    def perform_update(self, serializer):
       return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def partial_update(self, request, pk=None):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class AllProductsInOfferV2APIView(APIView, DefualtPaginationClass):

    def get(self, request, *args, **kwargs):
        today = self.request.query_params.get('today')
        yesterday = self.request.query_params.get('yesterday')
        custom_date = self.request.query_params.get('date')

        if request.user.is_authenticated:
            catagories_obj = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
            business_ids = list(models.Business.objects.filter(i_category__in=catagories_obj, is_claimed=2).exclude(i_user__is_active=False).values_list('id',flat=True))
            interest_query = Q(i_business__in=business_ids, is_active=True, is_expiry=False)
            banner_query = models.Banner.objects.filter(Q(is_active=True, position=7, language=request.user.lang_code) | Q(is_active=True, position=8, language=request.user.lang_code))
        else:
            interest_query = Q(is_active=True, is_expiry=False)
            if request.headers.get('Accept-Language') == str(1):
                banner_query = models.Banner.objects.filter(Q(is_active=True, position=7, language=1) | Q(is_active=True, position=8, language=1))
            else:
                banner_query = models.Banner.objects.filter(Q(is_active=True, position=7, language=2) | Q(is_active=True, position=8, language=2))

        banner_serializer = BannerListSerializer(banner_query, many=True)

        content_list = models.Content.objects.filter(is_active=True).exclude(Q(i_brand__is_active=False) | Q(i_business__i_user__is_active=False) | Q(i_sub_category__is_active=False) | Q(i_business__is_active=False)).values_list("id",flat=True)
        query = Q(interest_query, type=4, i_content__in=content_list)

        offer_main_query = models.Offers.objects
        today_date = datetime.now().date()
        yesterday_date = today_date - timedelta(days=1)
        if today or yesterday:
            date_query = Q(query, start__date=today) | Q(query, start__date=yesterday)
        elif custom_date:
            date_query = Q(query, start__date__lte=custom_date)
        else:
            date_query = query

        today_count = format_number(len(offer_main_query.filter(query, start__date=today_date, i_content__in=content_list).values_list('i_content',flat=True)))
        yesterday_count = format_number(len(offer_main_query.filter(query, start__date=yesterday_date, i_content__in=content_list).values_list('i_content',flat=True)))

        if custom_date:
            custom_date_count = format_number(len(offer_main_query.filter(query, start__date__lte=custom_date, i_content__in=content_list).values_list('i_content',flat=True)))
        else:
            custom_date_count = str(0)
        offers = offer_main_query.filter(date_query).order_by('-start__date').distinct()
        if offers:
            offer_serializer = OfferDetailSerializer(offers, context={"request": request}, many=True)
            offer_serializer = offer_serializer.data
            if offer_serializer:
                offer_list = []
                for offer in offer_serializer:
                    offer_list.extend(offer['result'])

            serializer = self.paginate_queryset(offer_list, self.request)

            return Response({'error': '', 'error_code': '',"today_count":today_count, "yesterday_count":yesterday_count, "custom_date_count":custom_date_count, "banner":banner_serializer.data , 'data': serializer,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No Offer found', 'error_code': '', "today_count":today_count, "yesterday_count":yesterday_count, "custom_date_count":custom_date_count, "banner":banner_serializer.data, 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
 
class AllFeaturedBusinessAPIView(viewsets.ModelViewSet):

    serializer_class = HomeBusinessWithAddressSerializer
    pagination_class = DefualtPaginationClass
    queryset = models.Business.objects.filter(is_active=True, is_featured=True).exclude(i_user__is_active=False).order_by('-updated_at')

    def list(self,request):     

        business_obj = models.Business.objects.filter(is_active=True, is_featured=True).exclude(i_user__is_active=False).order_by('-updated_at')

        context = {'request': request}

        business_obj = self.paginate_queryset(business_obj)

        all_featured_business_serializer = HomeBusinessWithAddressSerializer(business_obj, context= context,many=True)
        if all_featured_business_serializer:
            return Response({'error': [], 'error_code': '', 'data': all_featured_business_serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
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
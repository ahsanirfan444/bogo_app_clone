from rest_framework.response import Response
from hubur_apis import models
from rest_framework import status
from rest_framework import viewsets
from core.defaults import DefualtPaginationClass
from hubur_apis.serializers.content_serializer import ContentDetailSerializer
from hubur_apis.serializers.home_serializer import HomeBusinessWithAddressSerializer
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Case, When, Value, IntegerField
from hubur_apis.serializers.offer_serializer import HotOffersListSerializer, OffersHomeListSerializer
from hubur_apis.serializers.trending_discount_serializer import (
    TrendingDiscountSerializer
    )

class TrendingDiscount(viewsets.ModelViewSet):

    pagination_class = DefualtPaginationClass
    serializer_class = TrendingDiscountSerializer
    queryset = models.TrendingDiscount.objects.filter(is_active=True).order_by('-created_at')

    def list(self,request):
        trending_discount_list = models.TrendingDiscount.objects.filter(is_active=True).order_by('-created_at')
        trending_discount_list = self.paginate_queryset(trending_discount_list)
        trending_discount_serializer = TrendingDiscountSerializer(trending_discount_list, many=True)
        if trending_discount_serializer:
            return Response({'error': [], 'error_code': '', 'data': trending_discount_serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': ['No Data found'], 'error_code': 'HD404', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
    
    def retrieve(self, request, pk=None):
        if pk:
            try:
                pk = int(pk)
            except:
                return Response({'error': ['Not a valid id'], 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            queryset_list = list(models.TrendingDiscount.objects.filter(is_active=True).values_list('id',flat=True))
            if int(pk) in queryset_list:
                

                all_businesses_list = list(models.TrendingDiscount.objects.filter(id=pk).values_list('i_business', flat=True))
                last_week = timezone.now().date() - timedelta(days=7)
                all_checked_in = list(models.Checkedin.objects.filter(i_business__in=all_businesses_list, created_at__date__gte=last_week)\
                                .values_list('i_business_id')\
                                .annotate(checkin_count=Count('id'))\
                                .order_by('-checkin_count'))[:5]
                
                all_businesses_list = []
                for tup in all_checked_in:
                    all_businesses_list.append(tup[0])


                case_statement = Case(*[When(id=business_id, then=Value(total_count)) for business_id, total_count in all_checked_in],
                    default=Value(0),
                    output_field=IntegerField(),)
                
                if request.user.username:
                    user_cat_list = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
                    all_businesses = models.Business.objects.filter(id__in=all_businesses_list, is_active=True, i_category__in=user_cat_list).annotate(checkin_count=case_statement,).order_by('-checkin_count')
                else:
                    all_businesses = models.Business.objects.filter(is_active=True, id__in=all_businesses_list).annotate(checkin_count=case_statement,).order_by('-checkin_count')
                    
                serializer = HomeBusinessWithAddressSerializer(all_businesses, many=True)
                
                if serializer:
                    return Response({'error': [], 'error_code': '' ,'data': serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': ["No Result Found"], 'error_code':"" , 'data': "",'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': ["No Result Found"], 'error_code': '' , 'data': "",'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        
    def create(self, request, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
       
    def perform_update(self, serializer):
       return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        


class AllTrendingDiscount(viewsets.ModelViewSet):

    pagination_class = DefualtPaginationClass
    serializer_class = TrendingDiscountSerializer
    queryset = models.TrendingDiscount.objects.filter(is_active=True).order_by('-created_at')

    def retrieve(self, request, pk=None):
        queryset_list = list(models.TrendingDiscount.objects.filter(is_active=True).values_list('id',flat=True))
        try:
           pk = int(pk)
        except:
             return Response({'error': ['Not a valid id'], 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        if pk in queryset_list:
            all_businesses_list = list(models.TrendingDiscount.objects.filter(id=pk).values_list('i_business',flat=True))
            last_week = timezone.now().date() - timedelta(days=7)
            all_checked_in = list(models.Checkedin.objects.filter(i_business__in=all_businesses_list, created_at__date__gte=last_week)\
                            .values_list('i_business_id')\
                            .annotate(checkin_count=Count('id'))\
                            .order_by('-checkin_count'))
            
            all_businesses_list = [tup[0] for tup in all_checked_in]


            case_statement = Case(*[When(id=business_id, then=Value(total_count)) for business_id, total_count in all_checked_in],
                default=Value(0),
                output_field=IntegerField(),)
                    
            if request.user.username:
                user_cat_list = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
                all_businesses = models.Business.objects.filter(id__in=all_businesses_list, is_active=True, i_category__in=user_cat_list).annotate(checkin_count=case_statement,).order_by('-checkin_count')
                
            else:
                all_businesses = models.Business.objects.filter(is_active=True, id__in=all_businesses_list).annotate(checkin_count=case_statement,).order_by('-checkin_count')
            

            content_id_list = list(models.Offers.objects.filter(i_business__in=all_businesses, is_active=True, is_expiry=False, type=4)[:10].values_list("i_content",flat=True))
            content_obj = models.Content.objects.filter(id__in=content_id_list)[:4]
            content_serializer = ContentDetailSerializer(content_obj, many=True)

            business_serializer = HomeBusinessWithAddressSerializer(all_businesses[:4], many=True)
            business_serializer = business_serializer.data
            if business_serializer:
                data_dict = dict()
                data_dict['hot_offer'] = content_serializer.data
                data_dict['bussiness'] = business_serializer
                
                return Response({'error': [], 'error_code': '' ,'data': data_dict,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': ['No Data found'], 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': ['No Data found'], 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
    def create(self, request, *args, **kwargs):
            return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
       
    def perform_update(self, serializer):
       return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self,request):
       return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


class ViewAllTrendingDiscount(viewsets.ModelViewSet):

    pagination_class = DefualtPaginationClass
    serializer_class = TrendingDiscountSerializer
    queryset = models.TrendingDiscount.objects.filter(is_active=True).order_by('-created_at')

    def retrieve(self, request, pk=None):
        queryset_list = list(models.TrendingDiscount.objects.filter(is_active=True).values_list('id',flat=True))
        try:
           pk = int(pk)
        except:
             return Response({'error': ['Not a valid id'], 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            type_param = self.request.query_params.get('type')
            if type_param is not None:
                type_param = int(type_param)
            else:
                return Response({'error': ['type is not define'], 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            if type_param != 1 and type_param != 2:
                return Response({'error': ['Invalid type'], 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': ['Invalid type'], 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        if pk in queryset_list:
            all_businesses_list = list(models.TrendingDiscount.objects.filter(id=pk).values_list('i_business',flat=True))
            last_week = timezone.now().date() - timedelta(days=7)
            all_checked_in = list(models.Checkedin.objects.filter(i_business__in=all_businesses_list, created_at__date__gte=last_week)\
                            .values_list('i_business_id')\
                            .annotate(checkin_count=Count('id'))\
                            .order_by('-checkin_count'))
            
            all_businesses_list = [tup[0] for tup in all_checked_in]


            case_statement = Case(*[When(id=business_id, then=Value(total_count)) for business_id, total_count in all_checked_in],
                default=Value(0),
                output_field=IntegerField(),)
                    
            if request.user.username:
                user_cat_list = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))
                all_businesses = models.Business.objects.filter(id__in=all_businesses_list, is_active=True, i_category__in=user_cat_list).annotate(checkin_count=case_statement,).order_by('-checkin_count')
                
            else:
                all_businesses = models.Business.objects.filter(is_active=True, id__in=all_businesses_list).annotate(checkin_count=case_statement,).order_by('-checkin_count')
            
            if type_param == 1:
                content_id_list = list(models.Offers.objects.filter(i_business__in=all_businesses, is_active=True, is_expiry=False, type=4).values_list("i_content",flat=True))
                content_obj = models.Content.objects.filter(id__in=content_id_list)
                content_obj = self.paginate_queryset(content_obj)
                content_serializer = ContentDetailSerializer(content_obj, many=True)
                serializer_data = content_serializer.data
            else:
                all_businesses = self.paginate_queryset(all_businesses)
                business_serializer = HomeBusinessWithAddressSerializer(all_businesses, many=True)
                serializer_data = business_serializer.data
            
            return Response({'error': [], 'error_code': '' ,'data': serializer_data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': ['No Data found'], 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
    def create(self, request, *args, **kwargs):
            return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
       
    def perform_update(self, serializer):
       return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self,request):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
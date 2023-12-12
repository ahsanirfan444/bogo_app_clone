from hubur_apis import models
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from core.defaults import DefualtPaginationClass
from hubur_apis.serializers.brand_serializer import (
    BrandListSerializer,
    )
from hubur_apis.serializers.content_serializer import (
    ContentDetailSerializer,
    )
from hubur_apis.serializers.entity_details_serializer import (
    BusinessListSerializer,
    )
from hubur_apis.serializers.home_serializer import (
    LocationForGuestModeSerializer,
    )
from django.db.models import Q
class BrandsDetailView(viewsets.ModelViewSet):

    serializer_class = BrandListSerializer
    queryset = models.Brand.objects.filter(is_active=True)

    def retrieve(self, request, pk=None):
        if pk:
            try:
                pk = int(pk)
            except:
                return Response({'error': ['Not a valid id'], 'error_code': '', 'data': {},'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            queryset_list = list(models.Brand.objects.filter(is_active=True).values_list('id',flat=True))
            if int(pk) in queryset_list:
                serializer = BrandListSerializer(models.Brand.objects.get(id=pk), context={"request": request})
                return Response({'error': [], 'error_code': '','type':'brand' , 'data': serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': [], 'error_code': ["No Result Found"], 'type':'brand', 'data': "",'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': ["No Brand Found"], 'error_code': '', 'type':'brand', 'data': "",'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def list(self,request):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def update(self, request, pk, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
       
    def perform_update(self, serializer):
       return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class BusinessDetailView(viewsets.ModelViewSet):

    serializer_class = BusinessListSerializer
    queryset = models.Brand.objects.filter(is_active=True)

    def retrieve(self, request, pk=None):
        if pk:
            try:
                pk = int(pk)
            except:
                return Response({'error': ['Not a valid id'], 'error_code': '', 'data': {},'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            queryset_list = list(models.Business.objects.filter(is_active=True).exclude(i_user__is_active=False).values_list('id',flat=True))
            if int(pk) in queryset_list:
                if request.user.username:
                    business_obj = models.Business.objects.get(id=pk)
                    models.Visited.objects.get_or_create(**{'i_user':request.user,'i_business':business_obj})
                    serializer = BusinessListSerializer(business_obj, context = {'request': request})
                else:

                    if "lat" and "long" in request.GET:

                        user_long = request.GET['long']
                        user_lat = request.GET['lat']

                        location_serializer = LocationForGuestModeSerializer(data={"lat":user_lat,"long":user_long})
                        if location_serializer.is_valid():
                            user_lat = location_serializer.validated_data['lat']
                            user_long = location_serializer.validated_data['long']
                            
                            context = {"user_lat": user_lat,"user_long":user_long, 'request': request}
                            serializer = BusinessListSerializer(models.Business.objects.get(id=pk), context = context)     
                    else:
                        serializer = BusinessListSerializer(models.Business.objects.get(id=pk), context = {'request': request})
                
                data_dict = serializer.data
                if data_dict:
                    return Response({'error': [], 'error_code': '','type':data_dict['i_category'] ,'data': data_dict,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': ["No Result Found"], 'error_code':"" ,'type':"" , 'data': "",'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': ["No Business Found"], 'error_code': '','type':"" , 'data': "",'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def create(self, request, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def list(self,request):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def update(self, request, pk, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
       
    def perform_update(self, serializer):
       return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class ContentDetailView(viewsets.ModelViewSet):

    serializer_class = ContentDetailSerializer
    queryset = models.Content.objects.filter(is_active=True, i_sub_category__is_active=True).exclude(i_brand__is_active=False)

    def retrieve(self, request, pk=None):
        if pk:
            try:
                content_obj = models.Content.objects.get(is_active=True, i_user__is_active=True, i_business__is_active=True, i_business__i_user__is_active=True, id=pk)
                if request.user.is_authenticated:

                    context = {"content_detail":True, "user_obj":request.user, "request": request}
                else:
                    context = {"content_detail":True, "request": request}

            except:
                return Response({'error': ["No content found"], 'error_code': '','type':"" , 'data': "",'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(content_obj, context=context)
            
            you_may_like = models.Content.objects.filter(is_active=True, i_user__is_active=True, i_business__is_active=True, i_business=content_obj.i_business, i_sub_category__is_active=True).exclude(Q(i_brand__is_active=False) | Q(id=pk))[:5]
            you_may_like_serializer = self.get_serializer(you_may_like, many=True)
            
            return Response({'error': [], 'error_code': '','type':serializer.data['content_type'] , 'data': serializer.data,'you_may_like':you_may_like_serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def list(self,request):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def update(self, request, pk, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
       
    def perform_update(self, serializer):
       return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ViewAllBusinessProducts(viewsets.ModelViewSet):
    
    serializer_class = ContentDetailSerializer
    pagination_class = DefualtPaginationClass
    queryset = models.Content.objects.filter(is_active=True, i_sub_category__is_active=True).exclude(i_brand__is_active=False)

    def retrieve(self, request, pk=None):
        if pk:
            try:
                business_obj = models.Business.objects.get(is_active=True, i_user__is_active=True, id=pk)
                if business_obj.is_claimed == 1:
                    return Response({'error': ["This business is not claimed by anyone"], 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

            except:
                return Response({'error': ["No business found"], 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            
            all_products = models.Content.objects.filter(i_business=business_obj, is_active=True, i_sub_category__is_active=True).exclude(i_brand__is_active=False)
            all_products = self.paginate_queryset(all_products)
            serializer = self.get_serializer(all_products, many=True)
            
            return Response({'error': [], 'error_code': '' , 'data': serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def list(self,request):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def update(self, request, pk, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
       
    def perform_update(self, serializer):
       return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
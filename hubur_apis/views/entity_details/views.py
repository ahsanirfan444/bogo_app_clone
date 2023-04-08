from hubur_apis import models
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from hubur_apis.serializers.brand_serializer import BrandListSerializer
from hubur_apis.serializers.entity_details_serializer import (
    BusinessListSerializer,
)
from hubur_apis.serializers.home_serializer import LocationForGuestModeSerializer

class BrandsDetailView(viewsets.ModelViewSet):

    serializer_class = BrandListSerializer
    queryset = models.Brand.objects.filter(is_active=True)

    def retrieve(self, request, pk=None):
        if pk:
            queryset_list = list(models.Brand.objects.filter(is_active=True).values_list('id',flat=True))
            if int(pk) in queryset_list:
                serializer = BrandListSerializer(models.Brand.objects.get(id=pk))
                return Response({'error': [], 'error_code': '','type':'brand' , 'data': serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': [], 'error_code': ["No Result Found"], 'type':'brand', 'data': "",'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': ["No Brand Found"], 'error_code': '', 'type':'brand', 'data': "",'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
    
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

    serializer_class = BrandListSerializer
    queryset = models.Brand.objects.filter(is_active=True)

    def retrieve(self, request, pk=None):
        if pk:
            queryset_list = list(models.Business.objects.filter(is_active=True).values_list('id',flat=True))
            if int(pk) in queryset_list:
                if request.user.username:
                    serializer = BusinessListSerializer(models.Business.objects.get(id=pk), context = {'request': request})
                else:

                    if "lat" and "long" in request.GET:

                        user_long = request.GET['long']
                        user_lat = request.GET['lat']

                        location_serializer = LocationForGuestModeSerializer(data={"lat":user_lat,"long":user_long})
                        if location_serializer.is_valid():
                            user_lat = location_serializer.validated_data['lat']
                            user_long = location_serializer.validated_data['long']
                            
                            context = {"user_lat": user_lat,"user_long":user_long}
                            serializer = BusinessListSerializer(models.Business.objects.get(id=pk), context = context)
                    
                    else:
                        serializer = BusinessListSerializer(models.Business.objects.get(id=pk), context = {'request': request})
                
                data_dict = serializer.data
                if data_dict:
                    return Response({'error': [], 'error_code': '','type':data_dict['i_category'] ,'data': data_dict,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': ["No Result Found"], 'error_code':"" ,'type':"" , 'data': "",'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': ["No Business Found"], 'error_code': '','type':"" , 'data': "",'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
    
    
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


from hubur_apis import models
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from core.defaults import DefualtPaginationClass
from hubur_apis.serializers.offer_serializer import (
    BusinessOffersDetailSerializer,OfferDetailSerializer
    )

class OfferAPIView(viewsets.ModelViewSet):

    serializer_class = OfferDetailSerializer
    queryset = models.Offers.objects.filter(is_active=True, is_expiry=False)
    pagination_class = DefualtPaginationClass

    def retrieve(self, request, pk=None):
        if pk:
            offers = models.Offers.objects.filter(id=pk, is_active=True, is_expiry=False).first()
            if offers:
                serializer = self.get_serializer(offers)
                if serializer:
                    serializer = serializer.data['result']
                    serializer = self.paginate_queryset(serializer)
                else:
                    serializer = []
                return Response({'error': '', 'error_code': '', 'data': serializer,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        
        return Response({'error': '', 'error_code': '', 'data': "No Offer Found",'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)

    def list(self,request):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def create(self, request, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
       
    def perform_update(self, serializer):
       return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def partial_update(self, request, pk=None):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

class GetBusinessOfferAPIView(viewsets.ModelViewSet):

    serializer_class = BusinessOffersDetailSerializer
    queryset = models.Offers.objects.filter(is_active=True, is_expiry=False)
    pagination_class = DefualtPaginationClass

    def retrieve(self, request, pk=None):
        try:
            type_param = int(self.request.query_params.get('type'))
        except:
            return Response({'error': 'Invalid type', 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        if pk and type_param:
            business_obj = models.Business.objects.filter(id=pk, is_active=True).first()
            if business_obj:
                offers = models.Offers.objects.filter(i_business=business_obj,type=type_param, is_active=True, is_expiry=False)
                
                if offers:
                    offers = offers.order_by('-created_at')
                    serializer = self.get_serializer(offers, many=True)
                    serializer = self.paginate_queryset(serializer.data)
                    return Response({'error': '', 'error_code': '', 'data': serializer,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': '', 'error_code': '', 'data': ["No business Found"],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
                
        return Response({'error': '', 'error_code': '', 'data': ["No business found in this offer"],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

    def list(self,request):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def create(self, request, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk, *args, **kwargs):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
       
    def perform_update(self, serializer):
       return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def partial_update(self, request, pk=None):
        return Response({'error': ['Method is not allowed'], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

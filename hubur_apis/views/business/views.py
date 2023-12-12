from rest_framework.response import Response
from core.defaults import DefualtPaginationClass
from hubur_apis import models
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from hubur_apis.serializers.business_serializer import (
    ClaimBusinessSerializer,BusinessListSerializer
    )

class ClaimBusinessAPIView(APIView):
    pagination_class = DefualtPaginationClass
    
    def post(self, request):
        serializer_class = ClaimBusinessSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response({'error': [], 'error_code': '', 'data': [serializer_class.data],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            error = []
            for e in serializer_class.errors.values():
                if (e[0].find("object does not exist")!= -1):
                    error.append("Business not found")
                else:
                    error.append(e[0])
            return Response({'error': error, 'error_code': 'HD404', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

class GetAllBususiness(viewsets.ModelViewSet):

    serializer_class = BusinessListSerializer
    queryset = models.Business.objects.filter(is_active=True)
    pagination_class = DefualtPaginationClass
    
    def list(self,request):
        all_business_query = models.Business.objects.filter(is_active=True, i_category__is_active=True).exclude(i_user__is_active=False)
        if all_business_query:
            all_business_query = self.paginate_queryset(all_business_query)
            serializer = BusinessListSerializer(all_business_query, context={"request": request}, many=True)
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

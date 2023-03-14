from rest_framework.response import Response
from hubur_apis import models
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from hubur_apis.serializers.business_serializer import (
    ClaimBusinessSerializer,BusinessListSerializer
    )

class ClaimBusinessAPIView(APIView):

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


    def get(self, request):

        busines_obj = models.Business.objects.filter(is_active=True, is_claimed=1)
        context = {'request': request}
        busines_serializer = BusinessListSerializer(busines_obj, context= context,many=True)
        if busines_serializer:

            return Response({'error': [], 'error_code': '', 'data': busines_serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': ['No Business found'], 'error_code': '', 'data': {},'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

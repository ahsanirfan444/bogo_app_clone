from rest_framework.response import Response
from hubur_apis import models
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from hubur_apis.serializers.user_interest_serializer import (
    CreateUserInterestSerializer,UpdateUserInterestSerializer ,GetAllCategoriesSerializer,GetUserInterestSerializer
    )

class CreateUserInterestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer_class = CreateUserInterestSerializer(data=request.data, context={"user_obj":request.user})
        if serializer_class.is_valid():
            serializer_class.save()
            data_dict = dict()
            data_dict = serializer_class.data

            return Response({'error': [], 'error_code': "", 'data': data_dict,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            error_list = []
            for e in serializer_class.errors.values():
                if (e[0].find("object does not exist")!= -1):
                    error_list.append("Catagory not found")
                elif (e[0].find("Expected pk value, received str")!= -1):
                    error_list.append("id cannot be empty")
                else:
                    error_list.append(e[0])
            return Response({'error': error_list, 'error_code': 'HD404', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        user_obj = models.UserInterest.objects.filter(i_user=request.user).order_by("-created_at")
        if user_obj:
            user_obj = user_obj.first()
            serializer = GetUserInterestSerializer(user_obj, context={'request': request})
        
            if serializer.data:
                return Response({'error': [], 'error_code': '', 'data': [serializer.data],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        return Response({'error': [], 'error_code': '', 'data': ["No Result Found"],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            instance = models.UserInterest.objects.filter(i_user=request.user).order_by("-created_at")
            if instance:
                instance = instance.first()
                serializer = UpdateUserInterestSerializer(instance, data=request.data, context={"user_obj":request.user}, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    data_dict = dict()
                    data_dict = serializer.data
                    data_dict['i_category'] = data_dict['category']
                    del data_dict['category']

                    return Response({'error': [], 'error_code': '', 'data': [data_dict],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
                else:
                    error_list = []
                    for e in serializer.errors.values():
                        if (e[0].find("object does not exist")!= -1):
                            error_list.append("Catagory not found")
                        elif (e[0].find("Expected pk value, received str")!= -1):
                            error_list.append("id cannot be empty")
                        else:
                            error_list.append(e[0])
                    return Response({'error': error_list, 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            else:    
                return Response({'error': "No Interest found for this user", 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        except models.UserInterest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class GetCatagoriesListAPIView(APIView):

    def get(self, request):
        categories_query = models.Category.objects.filter(is_active=True)
        categories_serializer = GetAllCategoriesSerializer(categories_query, context={'request': request}, many=True)
        if categories_serializer.data:
            return Response({'error': [], 'error_code': '', 'data': categories_serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': [], 'error_code': '', 'data': ["No Result Found"],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
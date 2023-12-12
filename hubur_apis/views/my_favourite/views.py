from rest_framework.response import Response
from core.defaults import DefualtPaginationClass
from rest_framework.permissions import IsAuthenticated
from hubur_apis import models
from rest_framework import status
from rest_framework import viewsets
from django.db.models import Case, When
from hubur_apis.serializers.home_serializer import HomeBusinessWithAddressSerializer
from hubur_apis.serializers.my_fav_serializer import (
    MyFavSerializer ,
    )

class MyFavouriteView(viewsets.ModelViewSet):

    queryset = models.MyFavourite.objects.all()
    pagination_class = DefualtPaginationClass
    serializer_class = MyFavSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer_class = MyFavSerializer(data=request.data, context = {'user_obj':request.user})
        if serializer_class.is_valid():
            if 'deleted' in serializer_class.validated_data:
                return Response({'error': [], 'error_code': '', 'data': ["Removed from your Favourite Successfully"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                serializer_class.save()
                my_favourite_obj = serializer_class.instance
                
                models.MyFavourite.objects.create(**my_favourite_obj)
                return Response({'error': [], 'error_code': '', 'data': ["Added in your Favourite Successfully"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            error_list = []
            for e in serializer_class.errors.values():
                    error_list.append(e[0])
            return Response({'error': error_list, 'error_code': 'HD404', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
    def list(self, request, *args, **kwargs):
        user_obj = request.user.username
        if user_obj:

            all_business_list = list(models.MyFavourite.objects.filter(i_user=request.user).values_list("i_business",flat=True))
            all_business_dict = {id_val: pos for pos, id_val in enumerate(all_business_list)}
            whens = [When(id=id_val, then=pos) for id_val, pos in all_business_dict.items()]
            order_by = Case(*whens)
            all_business = models.Business.objects.filter(id__in=all_business_list, is_active=True).exclude(i_user__is_active=False).order_by(order_by)
            context = {'request': request}

            my_favourite_obj = self.paginate_queryset(all_business)
            my_favourite_serializer = HomeBusinessWithAddressSerializer(my_favourite_obj, context= context ,many=True)
            if my_favourite_serializer:
                return Response({'error': [], 'error_code': '', 'data': my_favourite_serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': [], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': [], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
             

             
   
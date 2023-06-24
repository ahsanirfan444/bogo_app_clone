from rest_framework.response import Response
from core.defaults import DefualtPaginationClass
from rest_framework.permissions import IsAuthenticated
from hubur_apis import models
from rest_framework import status
from rest_framework import viewsets
from django.db.models import Q,Case, When
from hubur_apis.serializers.bookmark_serializer import (
    BookmarkSerializer
    )
from hubur_apis.serializers.home_serializer import HomeBusinessWithAddressSerializer

class MyBookmarkView(viewsets.ModelViewSet):

    queryset = models.MyBookmark.objects.all()
    pagination_class = DefualtPaginationClass
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
     
        all_business_list = list(models.MyBookmark.objects.filter(i_user=request.user).values_list("i_business",flat=True).order_by("-created_at"))
        all_business_dict = {id_val: pos for pos, id_val in enumerate(all_business_list)}
        whens = [When(id=id_val, then=pos) for id_val, pos in all_business_dict.items()]
        order_by = Case(*whens)
        all_business = models.Business.objects.filter(id__in=all_business_list).order_by(order_by)

        context = {'request': request}

        my_bookmark_obj = self.paginate_queryset(all_business)
        my_bookmark_serializer = HomeBusinessWithAddressSerializer(my_bookmark_obj, context= context ,many=True)
        if my_bookmark_serializer:
            return Response({'error': [], 'error_code': '', 'data': my_bookmark_serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': [], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)


    def create(self, request):
        serializer_class = BookmarkSerializer(data=request.data, context = {'user_obj':request.user})
        if serializer_class.is_valid():
            if 'deleted' in serializer_class.validated_data:
                return Response({'error': [], 'error_code': '', 'data': ["Removed from your Bookmark Successfully"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                serializer_class.save()
                my_bookmark_obj = serializer_class.instance
                
                models.MyBookmark.objects.create(**my_bookmark_obj)
                return Response({'error': [], 'error_code': '', 'data': ["Added in your Bookmark Successfully"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            error_list = []
            for e in serializer_class.errors.values():
                    error_list.append(e[0])
            return Response({'error': error_list, 'error_code': 'HD404', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
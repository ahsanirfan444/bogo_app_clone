from rest_framework.response import Response
from core.defaults import DefualtPaginationClass
from rest_framework.permissions import IsAuthenticated
from hubur_apis import models
from rest_framework import status
from rest_framework import viewsets
from hubur_apis.serializers.content_serializer import ContentDetailSerializer
from hubur_apis.serializers.home_serializer import HomeBusinessWithAddressSerializer
from hubur_apis.serializers.saved_offer_serializer import (
    SavedOfferSerializer
    )

class SavedOfferView(viewsets.ModelViewSet):

    queryset = models.MyFavourite.objects.all()
    pagination_class = DefualtPaginationClass
    serializer_class = SavedOfferSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer_class = SavedOfferSerializer(data=request.data, context = {'user_obj':request.user})
        if serializer_class.is_valid():
            if 'deleted' in serializer_class.validated_data:
                return Response({'error': [], 'error_code': '', 'data': ["Removed from Saved Offer Successfully"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                serializer_class.save()
                saved_offer_obj = serializer_class.instance
                
                models.SavedOffers.objects.create(**saved_offer_obj)
                return Response({'error': [], 'error_code': '', 'data': ["Your Offer has been Saved Successfully"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            error_list = []
            for e in serializer_class.errors.values():
                    error_list.append(e[0])
            return Response({'error': error_list, 'error_code': 'HD404', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
    def list(self, request, *args, **kwargs):
        user_obj = request.user.username
        if user_obj:

            all_contents_list = list(models.SavedOffers.objects.filter(i_user=request.user, i_business__is_active=True, i_business__i_user__is_active=True).values_list("i_content",flat=True))
            all_contents = models.Content.objects.filter(id__in=all_contents_list, is_active=True, i_sub_category__is_active=True).exclude(i_brand__is_active=False)
            context = {'request': request}

            all_contents = self.paginate_queryset(all_contents)
            all_contents_serializer = ContentDetailSerializer(all_contents, context= context ,many=True)
            if all_contents_serializer:
                return Response({'error': [], 'error_code': '', 'data': all_contents_serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': [], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': [], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
             

             
   
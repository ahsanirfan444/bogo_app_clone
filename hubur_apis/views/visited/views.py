from rest_framework.response import Response
from core.defaults import DefualtPaginationClass
from rest_framework.permissions import IsAuthenticated
from hubur_apis import models
from rest_framework import status
from rest_framework import viewsets
from hubur_apis.serializers.save_business_serializer import VisitedBusinessSerializer
from django.db.models import Case, When

class MyVisitedView(viewsets.ModelViewSet):

    queryset = models.MyFavourite.objects.all()
    pagination_class = DefualtPaginationClass
    serializer_class = VisitedBusinessSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user_obj = request.user.username
        if user_obj:

            all_business_list = list(models.Visited.objects.filter(i_user=request.user).values_list("i_business",flat=True))
            all_business_dict = {id_val: pos for pos, id_val in enumerate(all_business_list)}
            whens = [When(id=id_val, then=pos) for id_val, pos in all_business_dict.items()]
            order_by = Case(*whens)
            all_business = models.Business.objects.filter(id__in=all_business_list, is_active=True).exclude(i_user__is_active=False).order_by(order_by)
            context = {'user_obj': request.user, "request": request}

            my_favourite_obj = self.paginate_queryset(all_business)
            my_favourite_serializer = VisitedBusinessSerializer(my_favourite_obj, context= context ,many=True)
            if my_favourite_serializer:
                return Response({'error': [], 'error_code': '', 'data': my_favourite_serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': [], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': [], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
             

             
   
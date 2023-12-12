from rest_framework.response import Response
from core.defaults import DefualtPaginationClass
from hubur_apis import models
from rest_framework import status
from rest_framework import viewsets
from django.db.models import Q
from hubur_apis.serializers.review_serializer import (
    ReviewsSerializer,GetAllReviewsSerializer,
    )
import notifications
from django.urls import reverse_lazy

class ReviewsView(viewsets.ModelViewSet):

    queryset = models.Reviews.objects.all()
    pagination_class = DefualtPaginationClass
    serializer_class = ReviewsSerializer
    http_method_names = ['get', 'post', 'delete', 'patch']

    def create(self, request):
        user_obj = request.user.is_authenticated
        if user_obj:
            serializer_class = ReviewsSerializer(data=request.data, context = {'user_obj':request.user})
            if serializer_class.is_valid():
                serializer_class.save()
                reviews_obj = serializer_class.instance
                models.Reviews.objects.create(**reviews_obj)

                business_id = serializer_class.instance['i_content'].i_business_id
                business_name = serializer_class.instance['i_content'].i_business.name
                content_id = serializer_class.instance['i_content'].id
                msg = request.user.get_name() + " gave review on content "+serializer_class.instance['i_content'].name

                notifications.sendNotificationToAdmin(msg,business_name+" Review",request.user.id,8,self.request.build_absolute_uri(reverse_lazy("business_reviews_by_admin", kwargs={"pk": int(business_id)})), content_id)

                return Response({'error': [], 'error_code': '', 'data': ["Your review has been submitted"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                error_list = []
                for e in serializer_class.errors.values():
                        error_list.append(e[0])
                return Response({'error': error_list, 'error_code': 'HD404', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)  
        else:
            return Response({"detail": "Authentication credentials were not provided."},status=status.HTTP_401_UNAUTHORIZED)
 
    def retrieve(self, request, pk=None):
        if pk:
            review_obj = models.Reviews.objects.filter(i_content__id=pk, i_business__i_user__is_active=True, i_content__is_active=True, i_business__is_active=True).exclude( Q(i_content__i_brand__is_active=False) | Q(i_content__i_sub_category__is_active=False))
            review_obj = self.paginate_queryset(review_obj)
            review_serializer = GetAllReviewsSerializer(review_obj,many=True)
            if review_serializer:
                return Response({'error': [], 'error_code': '', 'data': review_serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': [], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
    
    def partial_update(self, request,pk = None, *args, **kwargs):
        user_obj = request.user.is_authenticated
        if user_obj:
            if pk:
                try:
                    instance = models.Reviews.objects.get(id=pk, i_user=request.user)
                except:
                    return Response({'error': ["Not valid review"], 'error_code': 'HS002', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

                serializer = self.get_serializer(instance, data=request.data, partial=True)
                if serializer.is_valid():
                    self.perform_update(serializer)
                    return Response({'error': [], 'error_code': '', 'data': serializer.data, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
                else:
                    error_list = []
                    for e in serializer.errors.values():
                            error_list.append(e[0])
                    return Response({'error': error_list, 'error_code': 'HS002', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Authentication credentials were not provided."},status=status.HTTP_401_UNAUTHORIZED)
    
    def destroy(self, request,pk = None, *args, **kwargs):
        user_obj = request.user.is_authenticated
        if user_obj:
            if pk:
                review_obj = models.Reviews.objects.filter(id=pk, i_user=request.user)
                self.perform_destroy(review_obj)
                return Response({'error': [], 'error_code': '', 'data': ["Review deleted successfully"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Authentication credentials were not provided."},status=status.HTTP_401_UNAUTHORIZED)

    def list(self, request, *args, **kwargs):
        user_obj = request.user.is_authenticated
        if user_obj:
            all_reviews = models.Reviews.objects.filter(i_user=request.user, i_business__i_user__is_active=True, i_content__is_active=True, i_business__is_active=True).exclude( Q(i_content__i_brand__is_active=False) | Q(i_content__i_sub_category__is_active=False))
            review_serializer = GetAllReviewsSerializer(all_reviews,many=True)
            review_list = self.paginate_queryset(review_serializer.data)
            return Response({'error': [], 'error_code': '', 'data': review_list,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Authentication credentials were not provided."},status=status.HTTP_401_UNAUTHORIZED)
        



class BusinessReviewsView(viewsets.ModelViewSet):

    queryset = models.Reviews.objects.all()
    pagination_class = DefualtPaginationClass
    serializer_class = ReviewsSerializer
    http_method_names = ['get']

    def retrieve(self, request, pk=None):
        if pk:
            active_users = models.UserProfile.objects.filter(is_active=True)
            review_obj = models.Reviews.objects.filter(i_business=pk, i_business__is_active=True).exclude(Q(i_content__i_sub_category__is_active=False))
            review_obj = self.paginate_queryset(review_obj)
            review_serializer = GetAllReviewsSerializer(review_obj,many=True)
            if review_serializer:
                return Response({'error': [], 'error_code': '', 'data': review_serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': [], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
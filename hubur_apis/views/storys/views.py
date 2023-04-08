from rest_framework.response import Response
from core.defaults import DefualtPaginationClass
from hubur_apis import models
from rest_framework import status
from rest_framework import viewsets
from global_methods import distance
from hubur_apis.serializers.home_serializer import LocationForGuestModeSerializer
from hubur_apis.serializers.story_serializer import (
    BusinessStoryListSerializer, ImageSerializer, StoriesSerializer, StoryListSerializer
    )

class UploadViewSet(viewsets.ModelViewSet):

    queryset = models.Story.objects.filter(is_active=True)
    pagination_class = DefualtPaginationClass
    serializer_class = StoryListSerializer

    def create(self, request):
        if request.user.username:
            serializer_class = ImageSerializer(data=request.data, context = {'user_obj':request.user})
            if serializer_class.is_valid():
                serializer_class.save()
                story_obj = serializer_class.instance
                del story_obj['file']
                del story_obj['updated_user']
                if 'image' in story_obj:
                    del story_obj['image']
                if 'video' in story_obj:
                    del story_obj['video']
                if 'caption' in story_obj:
                    del story_obj['caption']
                models.Checkedin.objects.create(**story_obj)
                return Response({'error': [], 'error_code': '', 'data': ["Story Uploaded"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                error_list = []
                for e in serializer_class.errors.values():
                        error_list.append(e[0])

                return Response({'error': error_list, 'error_code': 'HD404', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': ['No user login'], 'error_code': 'HD404', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        
    def list(self,request):
        all_business_data = []
        if request.user.username:
            user_long = request.user.long
            user_lat = request.user.lat
            if user_long and user_lat:
                catagories_obj = list(models.UserInterest.objects.filter(i_user=request.user).values_list('i_category',flat=True))

                business_objs = models.Business.objects.filter(is_active=True, i_category__in=catagories_obj).order_by('-created_at')
                for business in business_objs:
                    total_distance = distance(user_long,user_lat,business.long,business.lat)
                    if float(total_distance) <= 10:
                        all_business_data.append(business)

                all_business_obj = self.paginate_queryset(all_business_data)
                business_serializer = StoryListSerializer(all_business_obj,many=True)
                return Response({'error': [], 'error_code': '', 'data': business_serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
                
            else:
                return Response({'error': [], 'error_code': '', 'data': ["Enable your location"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            if 'long' and 'lat' in request.GET:
                location_serializer = LocationForGuestModeSerializer(data=request.GET)
                if location_serializer.is_valid():
                    user_lat = location_serializer.validated_data['lat']
                    user_long = location_serializer.validated_data['long']
                    business_objs = models.Business.objects.filter(is_active=True).order_by('-created_at')
                    for business in business_objs:
                        total_distance = distance(user_long,user_lat,business.long,business.lat)
                        if float(total_distance) <= 10:
                            all_business_data.append(business)

                    all_business_obj = self.paginate_queryset(all_business_data)
                    business_serializer = StoryListSerializer(all_business_obj,many=True)
                    return Response({'error': [], 'error_code': '', 'data': business_serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
                else:
                    error_list = []
                    for error in location_serializer.errors.values():
                        error_list.append(error[0])
                    return Response({'error': error_list, 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': [], 'error_code': '', 'data': ["Enable your location"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            

    
    def retrieve(self, request, pk=None):
        if pk:
            business_obj = models.Business.objects.filter(id=pk, is_active=True).exists()
            if business_obj:

                story_obj = models.Story.objects.filter(is_active=True, i_business=pk).order_by("-created_at")
                serializer = self.paginate_queryset(story_obj)
                serializer = StoriesSerializer(serializer, many=True)

                return Response({'error': [], 'error_code': '','data': serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': ["No Business found"], 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
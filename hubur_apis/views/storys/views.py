from rest_framework.response import Response
from core.defaults import DefualtPaginationClass
from hubur_apis import models
from rest_framework import status
from rest_framework import viewsets, views
from global_methods import distance
from rest_framework.permissions import IsAuthenticated
from hubur_apis.serializers.home_serializer import LocationForGuestModeSerializer
from hubur_apis.serializers.story_serializer import (
     ImageSerializer, StoriesSerializer, StoryListSerializer, UserStoriesSerializer
    )
import notifications
from datetime import datetime,timedelta

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

                user_friend_list = list(models.FriendList.objects.filter(friends=request.user, is_active=True).values_list("i_user_id",flat=True))
                msg = str(request.user.get_name()) + " Uploaded a new story"
                msg_ar = str(request.user.get_name()) + " تم تحميل قصة جديدة"
                
                notifications.sendNotificationToMultipleUser(user_friend_list,msg=msg, msg_ar=msg_ar, title="Story", title_ar="قصة", sender_id=str(request.user.id),content_id=None,action='story_uploaded',
                                                        notification_type=4, activityAndroid="FLUTTER_NOTIFICATION_CLICK", activityIOS="FLUTTER_NOTIFICATION_CLICK", user_id=str(request.user.id), actions='story_uploaded')

                reward_point = models.RewardPoints.objects.filter(type=3)
                if reward_point:
                    models.UserReward.objects.create(i_user=request.user, i_business=story_obj['i_business'], i_point=reward_point[0])

                last_24_hours = datetime.now() - timedelta(hours=24)
                user_checkedin = models.Checkedin.objects.filter(i_user=story_obj['i_user'], i_business=story_obj['i_business'], created_at__gte=last_24_hours).exclude(i_business__i_user__is_active=False)
                if user_checkedin:
                    user_checkedin.update(i_story=story_obj['i_story'], updated_at=datetime.now())
                else:
                    if story_obj['i_business'].is_claimed == 2: models.Checkedin.objects.create(**story_obj) 
                return Response({'error': [], 'error_code': '', 'data': ["Story Uploaded"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                error_list = []
                for e in serializer_class.errors.values():
                        error_list.append(e[0])

                return Response({'error': error_list, 'error_code': 'HD404', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        
    def list(self,request):
        all_business_data = []
        if request.user.username:
            user_long = request.user.long
            user_lat = request.user.lat
            if user_long or user_lat == None:
                return Response({'error': [], 'error_code': '', 'data': ["Enable your location"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            if 'long' and 'lat' in request.GET:
                location_serializer = LocationForGuestModeSerializer(data=request.GET)
                if location_serializer.is_valid():
                    user_lat = location_serializer.validated_data['lat']
                    user_long = location_serializer.validated_data['long']
                else:
                    error_list = []
                    for error in location_serializer.errors.values():
                        error_list.append(error[0])
                    return Response({'error': error_list, 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': [], 'error_code': '', 'data': ["Enable your location"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        
        business_objs = models.Business.objects.filter(is_active=True).exclude(i_user__is_active=False).order_by('-created_at')
        for business in business_objs:
            total_distance = distance(user_long,user_lat,business.long,business.lat)
            if float(total_distance) <= 10:
                all_business_data.append(business)

        all_business_obj = self.paginate_queryset(all_business_data)
        business_serializer = StoryListSerializer(all_business_obj,many=True)
        return Response({'error': [], 'error_code': '', 'data': business_serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            
    def retrieve(self, request, pk=None):
        if pk:
            business_obj = models.Business.objects.filter(id=pk, is_active=True).exclude(i_user__is_active=False).exists()
            if business_obj:

                story_obj = models.Story.objects.filter(is_active=True,i_user__is_active=True, i_business=pk).order_by("-created_at")
                serializer = self.paginate_queryset(story_obj)
                serializer = StoriesSerializer(serializer, many=True)

                return Response({'error': [], 'error_code': '','data': serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': ["No Business found"], 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            

class UserStoryViewSet(viewsets.ModelViewSet):

    queryset = models.Story.objects.filter(is_active=True)
    pagination_class = DefualtPaginationClass
    serializer_class = StoryListSerializer

    def retrieve(self,request, pk=None):
        if pk:
            story_obj = models.Story.objects.filter(i_user=pk, i_business__is_active=True).exclude(i_business__i_user__is_active=False)
            story_obj = self.paginate_queryset(story_obj)
            serializer = UserStoriesSerializer(story_obj,many=True)
            return Response({'error': [], 'error_code': '', 'data': serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)       
        else:
            return Response({'error': [], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            story_obj = models.Story.objects.filter(i_user=request.user, i_business__is_active=True).exclude(i_business__i_user__is_active=False)
            story_obj = self.paginate_queryset(story_obj)
            serializer = UserStoriesSerializer(story_obj,many=True)
            return Response({'error': [], 'error_code': '', 'data': serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)       
        else:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

class DeleteStory(viewsets.ModelViewSet):

    queryset = models.Story.objects.filter(is_active=True)
    serializer_class = StoryListSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
      
        try:
            story_obj = models.Story.objects.get(id=pk, i_user=request.user)
            models.Checkedin.objects.filter(i_story=story_obj).delete()
            story_obj.delete()
            return Response({'error': [], 'error_code': '', 'data': ["Successfully Deleted"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except:
            return Response({'error': ["Story not found"], 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, *args, **kwargs):
        return Response({'error': ["Method not allowed"], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def create(self, request, *args, **kwargs):
        return Response({'error': ["Method not allowed"], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def destroy(self, request, *args, **kwargs):
        return Response({'error': ["Method not allowed"], 'error_code': '', 'data': [],'status':status.HTTP_405_METHOD_NOT_ALLOWED}, status=status.HTTP_4HTTP_405_METHOD_NOT_ALLOWED0_BAD_REQUEST)
        

class ViewSingleStoryView(views.APIView):
    def get(self, request,pk, *args, **kwargs):
        try:
            if pk:
                queryset = models.Story.objects.get(id=pk)
                serializer = UserStoriesSerializer(queryset)
                serializer_data = serializer.data
                return Response({'error': [], 'error_code': '', 'data': [serializer_data], 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except:
            return Response({'error': ['No story found'], 'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

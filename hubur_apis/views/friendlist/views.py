from rest_framework.response import Response
from core.defaults import DefualtPaginationClass
from rest_framework.permissions import IsAuthenticated
from hubur_apis import models
from rest_framework import status
from rest_framework import viewsets
from hubur_apis.serializers.chat_serializer import UserInfoForChatSerializer
from hubur_apis.serializers.friendlist_serializer import CreateFriendSerializer, SerializerForUserFriendList
import notifications

class FriendListView(viewsets.ModelViewSet):

    queryset = models.FriendList.objects.all()
    pagination_class = DefualtPaginationClass
    serializer_class = CreateFriendSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):

        friend_list_obj = models.FriendList.objects.filter(i_user=request.user, is_active=True, friends__is_active=True)
        if friend_list_obj:

            friend_list_obj = self.paginate_queryset(friend_list_obj)

            serializer = SerializerForUserFriendList(friend_list_obj,many=True)
        
            if serializer:
                return Response({'error': [], 'error_code': '', 'data': serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': [], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': ["No friends found"], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
             
    def create(self, request, *args, **kwargs):

        content = {
            "user_obj":request.user 
        }
        serializer = self.get_serializer(data=request.data, context = content)
        if serializer.is_valid():
            
            user = request.user
            title = "Follow Notification"
            title_ar = "اتبع الإخطار"

            if 'deleted' in serializer.validated_data:
                
                return Response({'error': [], 'error_code': '', 'data': ["Unfollowed Successfully"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                msg = f"{user.get_name()} has start following you"
                msg_ar = f"{user.get_name()} بدأ في متابعتك"
                
                serializer.save()
                follow_user = serializer.data['friends']
                sender_pic = UserInfoForChatSerializer(request.user).data['profile_picture']
                notifications.sendNotificationToSingleUser(follow_user, msg, msg_ar, title, title_ar, request.user.id, None, 'follow', notification_type=2, activityAndroid="FLUTTER_NOTIFICATION_CLICK", activityIOS="FLUTTER_NOTIFICATION_CLICK",code=None  ,
                                                        sender_name=user.get_name(), image=sender_pic, sender=str(user.id), actions='follow')

                return Response({'error': [], 'error_code': '', 'data': ["Followed Successfully"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            error_list = []
            for e in serializer.errors.values():
                error_list.append(e[0])
            return Response({'error': error_list, 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

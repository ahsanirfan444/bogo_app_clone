from rest_framework.response import Response
from core.defaults import DefualtPaginationClass
from rest_framework.permissions import IsAuthenticated
from hubur_apis import models
from django.db.models import Q
from rest_framework import status,viewsets, views
from hubur_apis.serializers.chat_serializer import ChatListSerializer, MessagesListSerializer, CreateChannelIDSerializer
from math import ceil

class ChatView(viewsets.ModelViewSet):

    queryset = models.Chat.objects.all()
    pagination_class = DefualtPaginationClass
    serializer_class = ChatListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        
        user_obj = request.user

        query = Q(user_1=user_obj) | Q(user_2=user_obj)
        channel_id_list = list(models.Chat.objects.filter(query).values_list("channel_id",flat=True))

        received_channel_ids = list(set(models.Message.objects.filter(receiver=user_obj, channel_id__in =channel_id_list).values_list("channel_id",flat=True)))
        send_channel_ids = list(set(models.Message.objects.filter(sender=user_obj, channel_id__in =channel_id_list).values_list("channel_id",flat=True).exclude(channel_id__in=received_channel_ids)))

        
        
        receiver_chat_obj = models.Chat.objects.filter(Q(channel_id__in=received_channel_ids, is_read=False ,user_1=user_obj) | Q(channel_id__in=received_channel_ids, is_read=False, user_2=user_obj)).order_by("-count")

        sender_chat_obj = models.Chat.objects.filter(Q(channel_id__in=send_channel_ids) | Q(channel_id__in=received_channel_ids)).exclude(id__in=list(receiver_chat_obj.values_list("id",flat=True))).order_by("-updated_at")

        


        chat_obj = receiver_chat_obj | sender_chat_obj

        # chat_obj = {**receiver_chat_obj, **sender_chat_obj}

        chat_obj = self.paginate_queryset(chat_obj)
        content = {"user_obj":user_obj}
        chat_serializer = self.get_serializer(chat_obj, context=content, many=True)
        if chat_serializer:
            return Response({'error': [], 'error_code': '', 'data': chat_serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': [], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        
    def retrieve(self, request, pk=None):
        if pk:
            channel_id = pk

            chat_obj = models.Message.objects.filter(channel_id=channel_id)
            if chat_obj.exists():
                user_obj = request.user
                chat_obj = chat_obj[0]
                if chat_obj.receiver.id == user_obj.id:
                    receiver_user = chat_obj.sender
                else:
                    receiver_user = chat_obj.receiver
                user_status_obj = models.UserOnlineStatus.objects.filter(i_user=receiver_user)
                if user_status_obj.exists():
                    receiver_user_status = user_status_obj[0].is_online
                else:
                    receiver_user_status = False

                message_obj = models.Message.objects.filter(channel_id=channel_id).order_by("-created_at")
                page = reversed(self.paginate_queryset(message_obj))
                total_pages = ceil(message_obj.count() / 10)
            
                message_obj_serializer = MessagesListSerializer(page, context=user_obj, many=True)
                return Response({'error': [], 'error_code': '','receiver_user_status':receiver_user_status,"total_pages":total_pages ,'data': message_obj_serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': ["No channel id found"], 'error_code': '','receiver_user_status':False,"total_pages":0 , 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': ["No channel id found"], 'error_code': '','receiver_user_status':False,"total_pages":0 , 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    

class CreateChannelIDView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if 'receiver_id' in request.data:
            context = {"sender_id":request.user.id,"receiver_id":request.data['receiver_id']}
            serializer = CreateChannelIDSerializer(data=request.data, context=context)
            if serializer.is_valid():
                return Response({'error': [], 'error_code': '', 'data': serializer.validated_data['channel_id'],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': [], 'error_code': '', 'data': "",'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': ["receiver_id is not given"], 'error_code': '', 'data': "",'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

class IsReadView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        if "channel_id" in request.GET:
            channel_id = request.GET.get("channel_id")
            chat_obj = models.Chat.objects.filter(channel_id=channel_id)
            if chat_obj:
                chat_obj = chat_obj.first()
                chat_obj.count = int(0)
                chat_obj.is_read = True
                chat_obj.save()


                return Response({'error': [], 'error_code': '', 'data': "Successfully Read",'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': ["No channel id found"], 'error_code': '', 'data': "",'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': ["No channel id found"], 'error_code': '', 'data': "",'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

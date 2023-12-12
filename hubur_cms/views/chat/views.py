from django.db.models import Q
from django.http import JsonResponse
from django.conf import settings
from django.utils.decorators import method_decorator
from core.decorators import vendor_required
from rest_framework.authtoken.models import Token
from core.base import AuthBaseViews
from hubur_apis import models
import global_methods
from django.urls import reverse_lazy
from hubur_apis.serializers.chat_serializer import ChatListSerializer
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

@method_decorator([vendor_required], name="dispatch")
class all_rooms(AuthBaseViews):
    TEMPLATE_NAME = "chat/chat_module.html"

    def get(self, request, *args, **kwargs):
        try:
            content = {"user_obj":request.user}
            user_chats = models.Chat.objects.filter(Q(user_1=request.user) | Q(user_2=request.user))
            serializer = ChatListSerializer(user_chats, context=content, many=True)

            return self.render({'channels': serializer.data})
        except Exception:
            return self.render({'channels': ''})

@method_decorator([vendor_required], name="dispatch")
class room_detail(AuthBaseViews):
    TEMPLATE_NAME = "chat/chat_module_details.html"

    def get(self, request, user_id, *args, **kwargs):
        try:
            user_is_patient = models.UserProfile.objects.filter(id=user_id)
            if user_is_patient.exists():

                admin_profile_pic = self.request.user.profile_picture
                query = (Q(user_1=request.user) & Q(user_2=user_id)) | (Q(user_2=request.user) & Q(user_1=user_id))
                try:
                    current_channel = models.Chat.objects.get(query)
                except models.Chat.DoesNotExist:
                    current_channel = models.Chat.objects.create(user_1=request.user, user_2_id=user_id, channel_id=str(request.user.id)+"_"+str(user_id))

                channel_id = current_channel.channel_id

                messages = models.Message.objects.filter(channel_id=channel_id).order_by('created_at')

                online_status = models.UserOnlineStatus.objects.get(i_user=user_id).is_online
                last_seen = models.UserOnlineStatus.objects.get(i_user=user_id).updated_at
                
                if not current_channel.is_read:
                    current_channel.is_read = True
                    current_channel.count = 0
                    current_channel.save()
                
                content = {"user_obj":request.user}
                serializer = ChatListSerializer(current_channel, context=content)

                payload = jwt_payload_handler(request.user)
                token = jwt_encode_handler(payload)

                user_chats = models.Chat.objects.filter(Q(user_1=request.user) | Q(user_2=request.user))
                chat_serializer = ChatListSerializer(user_chats, context=content, many=True)

                return self.render({'channels': chat_serializer.data, 'channel': serializer.data, 'messages_list': messages, 'admin_profile_pic': admin_profile_pic, "token":token, "user_id": user_id, 'online_status': online_status, 'last_seen': last_seen})
            
            else:
                return self.redirect(reverse_lazy('chat'))

        except Exception:
            return self.redirect(reverse_lazy('chat'))
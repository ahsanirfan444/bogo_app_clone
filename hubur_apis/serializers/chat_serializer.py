from hubur_apis import models
from rest_framework import serializers
from django.db.models import Q

from hubur_apis.serializers.story_serializer import BusinessLogoSerializer, UserPicSerializer


class UserInfoForChatSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    business_id = serializers.SerializerMethodField(None)

    class Meta:
        model = models.UserProfile
        fields = ('id','profile_picture','name','role',"business_id")
    
    def get_name(self,obj):
        business = models.Business.objects.filter(i_user=obj.id)
        if business.exists():
            business = business.first()
            return business.name
        else:
            return obj.get_name()
    
    def get_business_id(self,obj):
        business = models.Business.objects.filter(i_user=obj.id)
        if business.exists():
            business = business.first()
            return business.id

    
    def get_profile_picture(self,obj):
        business = models.Business.objects.filter(i_user=obj.id)
        if business.exists():
            business = business.first()
            logo_pic = BusinessLogoSerializer(business).data['logo_pic']
            return logo_pic
        else:
            logo_pic = UserPicSerializer(obj).data['profile_picture']
            return logo_pic
    
    def get_role(self,obj):
        return obj.get_role_display()

class ChatListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
         model = models.Chat
         fields = ("user","is_read","channel_id","count","updated_at","last_message",)
    
    def get_user(self,obj):
        login_user = self.context.get("user_obj")
        if obj.user_1.id != login_user.id:
            response = UserInfoForChatSerializer(obj.user_1).data
        elif obj.user_2.id != login_user.id:
            response = UserInfoForChatSerializer(obj.user_2).data
        else:
            response = {}

        return response
        
    
    def get_count(self,obj):
        login_user = self.context.get("user_obj")
        messages = models.Message.objects.filter(channel_id=obj.channel_id).order_by("-created_at").first()
        if messages.sender == login_user:
            return 0
        else:
            return obj.count
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['last_msg_send'] = response['updated_at']
        del response['updated_at']
        return response


class MessagesListSerializer(serializers.ModelSerializer):
    sender_id = serializers.IntegerField(source="sender.id")
    sender_name = serializers.SerializerMethodField()
    sender_profile_pic = serializers.SerializerMethodField()
    receiver_id = serializers.IntegerField(source="receiver.id")
    receiver_name = serializers.SerializerMethodField()
    receiver_profile_pic = serializers.SerializerMethodField()
    msg_type = serializers.SerializerMethodField()

    class Meta:
         model = models.Message
         fields = ("id","sender_id","sender_name","sender_profile_pic","receiver_id","receiver_name","receiver_profile_pic","msg_type","channel_id","content","share_data","attachment","created_at",)

    
    def get_sender_name(self,obj):
        business = models.Business.objects.filter(i_user=obj.sender.id)
        if business.exists():
            business = business.first()
            return business.name
        else:
            response = obj.sender.get_name()
            return response
    
    def get_receiver_name(self,obj):
        business = models.Business.objects.filter(i_user=obj.receiver.id)
        if business.exists():
            business = business.first()
            return business.name
        else:
            response = obj.receiver.get_name()
            return response
    
    def get_msg_type(self,obj):
        return obj.type
    
    def get_sender_profile_pic(self,obj):
        response = UserInfoForChatSerializer(obj.sender).data['profile_picture']
        return response
    
    def get_receiver_profile_pic(self,obj):
        response = UserInfoForChatSerializer(obj.receiver).data['profile_picture']
        return response
    
class CreateMessagesSerializer(serializers.ModelSerializer):
    msg_type = serializers.IntegerField()
    receiver_id = serializers.IntegerField()
    type = serializers.IntegerField(required=False)
    sender = serializers.IntegerField(required=False)
    content = serializers.CharField(allow_blank=False, allow_null=False)
    attachment = serializers.CharField(allow_blank=True, allow_null=True)
    socket_url = serializers.CharField(required=False)
    class Meta:
        model = models.Message
        fields = ("sender","receiver_id","channel_id","msg_type","type","content","share_data","attachment","socket_url",)

    def validate(self, attrs):
        attrs['sender'] = self.context.get("user_ob")
        attrs['type'] = attrs['msg_type']
        del attrs['msg_type']
        return super().validate(attrs)
    

class CreateChannelIDSerializer(serializers.Serializer):
    channel_id = serializers.IntegerField(required=False)
    class Meta:
        model = models.Chat
        fields = ("channel_id",)

    
    def validate(self, attrs):
        sender_id = str(self.context.get("sender_id"))
        receiver_id = str(self.context.get("receiver_id"))
        channel_id = sender_id+"_"+receiver_id
        reversed_channel_id = '_'.join(channel_id.split('_')[::-1])

        query = Q(channel_id = channel_id) | Q(channel_id = reversed_channel_id)

        chat_obj = models.Chat.objects.filter(query)
        if chat_obj.exists():
            attrs['channel_id'] = chat_obj.first().channel_id
        else:
            attrs['channel_id'] = channel_id

        return super().validate(attrs)
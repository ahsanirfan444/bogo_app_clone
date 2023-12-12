
from hubur_apis import models
from rest_framework import serializers
from hubur_apis.serializers.content_serializer import ContentDetailSerializer

from hubur_apis.serializers.story_serializer import BusinessLogoSerializer, UserPicSerializer


class VotingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Voting
        fields = ("vote","i_business",)
    
    def create(self, validated_data):
        user_obj = self.context.get('user_obj')
        validated_data['i_user'] = user_obj
        return validated_data


    def validate(self, data):
        user_obj = self.context.get('user_obj')
        business = data['i_business']
        is_claimed = business.is_claimed
        if is_claimed == 1:
            raise serializers.ValidationError("This business is not claimed by anyone")
        voted_business = models.Voting.objects.filter(i_user=user_obj,i_business=business).exists()
        if voted_business:
            raise serializers.ValidationError("You have already vote this business")
        else:
            return data
        


class NotificationSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id')
    user_name = serializers.SerializerMethodField()
    sender_id = serializers.IntegerField(source='sender.id')
    image = serializers.SerializerMethodField()
    sender_name = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('context')
        super().__init__(*args, **kwargs)
        
        try:
            request = self.context.get('request')
            if request.user.is_authenticated:
                if request.user.lang_code == 1:
                    del self.fields['title_ar']
                    del self.fields['body_ar']
                else:
                    self.fields['title'] = self.fields['title_ar']
                    self.fields['body'] = self.fields['body_ar']

            else:
                if request.headers.get('Accept-Language') == str(1):
                    del self.fields['title_ar']
                    del self.fields['body_ar']
                else:
                    self.fields['title'] = self.fields['title_ar']
                    self.fields['body'] = self.fields['body_ar']

        except Exception as e:
            # print(e)
            pass

    class Meta:
        model = models.Notification
        fields = ('id','user_id','user_name','notification_type','code','is_read','sender_id','sender_name','image','content','title', 'title_ar', 'body', 'body_ar','reviewed','action','created_at','is_active',)

    def get_user_name(self,obj):
        return obj.user.get_name()
    
    def get_sender_name(self,obj):
        return obj.sender.get_name()
    
    def get_content(self,obj):
        request = self.context.get('request')
        if obj.content:
            return ContentDetailSerializer(obj.content, context={"request": request}).data
        else:
            return {}
    def get_image(self,obj):
        logo_pic = UserPicSerializer(obj.sender).data['profile_picture']
        return logo_pic
    
    def get_is_active(self, obj):
        response = False
        if obj.content:
            if obj.content.i_brand:
                if obj.content.is_active and obj.content.i_business.is_active and obj.content.i_business.i_user.is_active and obj.content.i_brand.is_active:
                    return True
            else:
                if obj.content.is_active and obj.content.i_business.is_active and obj.content.i_business.i_user.is_active:
                    return True
            return response
        else:
            return obj.sender.is_active
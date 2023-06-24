
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

    class Meta:
        model = models.Notification
        fields = ('id','user_id','user_name','notification_type','sender_id','sender_name','image','content','title','body','reviewed','action','created_at',)

    def get_user_name(self,obj):
        return obj.user.get_name()
    
    def get_sender_name(self,obj):
        return obj.sender.get_name()
    
    def get_content(self,obj):
        if obj.content:
            return ContentDetailSerializer(obj.content).data
        else:
            return {}
    def get_image(self,obj):
        logo_pic = UserPicSerializer(obj.sender).data['profile_picture']
        return logo_pic

from hubur_apis import models
from rest_framework import serializers

from hubur_apis.serializers.story_serializer import UserPicSerializer



class CreateFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FriendList
        fields = ("friends",)
    
    def create(self, validated_data):
        user_obj = self.context.get('user_obj')
        models.FriendList.objects.get_or_create(i_user=user_obj, friends=validated_data['friends'])
        return validated_data
    
    def validate(self, attrs):
        user_obj = self.context.get('user_obj')
        if attrs['friends']:
            if attrs['friends'] == user_obj:
                raise serializers.ValidationError("This user can not become your friend")
        
        my_friend = models.FriendList.objects.filter(i_user=user_obj, friends=attrs['friends'])
        if my_friend:
            my_friend.delete()
            status = {"deleted":True,"friend":attrs['friends']}
            return status
        else:
            return super().validate(attrs)
    
    

class SerializerForUserFriendList(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    class Meta:
        model = models.FriendList
        fields = ("id","name","profile_picture",)
    
    def get_name(self,obj):
        return obj.friends.get_name()
    
    def get_profile_picture(self, obj):
        profile_pic = UserPicSerializer(obj.friends).data['profile_picture']
        return profile_pic
    
    def get_id(self, obj):
        return obj.friends.id

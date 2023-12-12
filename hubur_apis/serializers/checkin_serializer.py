
from hubur_apis import models
from rest_framework import serializers
from datetime import datetime, timedelta, timezone
from django.utils.timesince import timesince
from hubur_apis.serializers.story_serializer import BusinessLogoSerializer

class CheckinSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Checkedin
        fields = ['i_business','other']

    def create(self, validated_data):
        user_obj = self.context.get('user_obj')
        validated_data['i_user'] = user_obj
        models.Checkedin.objects.create(**validated_data)
        return validated_data
        
    def validate(self, data):
        user_obj = self.context.get('user_obj')
        is_claimed = data['i_business'].is_claimed
        if is_claimed == 1:
            raise serializers.ValidationError("This business is not claimed by anyone")
        is_active = data['i_business'].is_active
        if is_active == False:
            raise serializers.ValidationError("This business is not active")
        
        checkin_exist = models.Checkedin.objects.filter(i_user=user_obj,i_business=data['i_business'])
        if checkin_exist:
            checkin_exist = checkin_exist.order_by('-created_at').first()
            cr_time = checkin_exist.created_at
            t2 = cr_time + timedelta(hours=24)
            now = datetime.now(timezone.utc)
            if now < t2:
                raise serializers.ValidationError("Already Check In for this business")
            else:
                return super().validate(data)
            
        else:
            return super().validate(data)


class GetCheckinListSerializer(serializers.ModelSerializer):
    business_id = serializers.CharField(source="i_business.id")
    business_name = serializers.CharField(source="i_business.name")
    business_address = serializers.CharField(source="i_business.address")
    business_category = serializers.CharField(source="i_business.i_category.name")
    business_logo = serializers.SerializerMethodField()
    class Meta:
        model = models.Checkedin
        fields = ["business_id","business_name","business_address","business_category","business_logo","updated_at",]

    def get_business_logo(self, obj):
        logo_pic = BusinessLogoSerializer(obj.i_business).data['logo_pic']
        return logo_pic
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
    
        now = datetime.now(timezone.utc) 
        checkin_creation_time = datetime.strptime(response['updated_at'], "%Y-%m-%dT%H:%M:%S.%f%z")

        time_difference = timesince(checkin_creation_time, now)
        response['checkin_time'] = time_difference + " ago"
        del response['updated_at'] 

        return response

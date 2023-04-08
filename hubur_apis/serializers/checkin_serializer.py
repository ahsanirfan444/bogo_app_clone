
from hubur_apis import models
from rest_framework import serializers
from datetime import datetime, timedelta, timezone

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





from hubur_apis import models
from rest_framework import serializers

class CheckinSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Checkedin
        fields = ['i_business','other']

    def create(self, validated_data):
        user_obj = self.context.get('user_obj')
        validated_data['i_user'] = user_obj
        models.Checkedin.objects.create(**validated_data)
        return validated_data

    def validate_i_business(self,value):
        business_obj = models.Business.objects.filter(id=value.id, is_active=True).exists()
        if business_obj:
            return value
        else:
            raise serializers.ValidationError("No Business Found")


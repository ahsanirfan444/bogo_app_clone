
from hubur_apis import models
from rest_framework import serializers

from hubur_apis.serializers.story_serializer import BusinessLogoSerializer


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
        voted_business = models.Voting.objects.filter(i_user=user_obj,i_business=business).exists()
        if voted_business:
            raise serializers.ValidationError("You have already vote this business")
        else:
            if business.is_active:
                if business.i_user:
                    if business.i_user.is_active:
                        return data
                    else:
                        raise serializers.ValidationError("This business is temporary Blocked by Admin")
                else:
                    return data
            else:
                raise serializers.ValidationError("This business is temporary Blocked by Admin")
            
            


        


class GetAllVotingSerializer(serializers.ModelSerializer):
    business_id = serializers.CharField(source="i_business.id")
    business_name = serializers.CharField(source="i_business.name")
    business_address = serializers.CharField(source="i_business.address")
    business_category = serializers.CharField(source="i_business.i_category.name")
    business_logo = serializers.SerializerMethodField()

    class Meta:
        model = models.Voting
        fields = ("vote","business_id","business_name","business_address","business_category","business_logo",)

    def get_business_logo(self, obj):
        logo_pic = BusinessLogoSerializer(obj.i_business).data['logo_pic']
        return logo_pic
    
    def to_representation(self, instance):
        return super().to_representation(instance)
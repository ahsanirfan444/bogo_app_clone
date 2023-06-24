
from hubur_apis import models
from rest_framework import serializers



class SavedOfferSerializer(serializers.ModelSerializer):
    i_business = serializers.IntegerField(read_only=True)
    class Meta:
        model = models.SavedOffers
        fields = ("i_business","i_content",)
    
    def create(self, validated_data):
        user_obj = self.context.get('user_obj')
        validated_data['i_user'] = user_obj
        validated_data['i_business'] = validated_data['i_content'].i_business
        return validated_data


    def validate(self, data):
        user_obj = self.context.get('user_obj')
        content = data['i_content']
        business = content.i_business
        saved_offer_obj = models.SavedOffers.objects.filter(i_user=user_obj,i_business=business, i_content=content)
        if saved_offer_obj:
            saved_offer_obj.delete()
            status = {"deleted":True}
            return status
        else:
            offer = models.Offers.objects.filter(i_content=content, is_active=True, is_expiry=False)
            if offer:
                return super().validate(data)
            else:
                raise serializers.ValidationError("Offer is not valid for this content")
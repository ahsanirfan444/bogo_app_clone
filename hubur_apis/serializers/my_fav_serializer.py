
from hubur_apis import models
from rest_framework import serializers



class MyFavSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MyFavourite
        fields = ("i_business",)
    
    def create(self, validated_data):
        user_obj = self.context.get('user_obj')
        validated_data['i_user'] = user_obj
        return validated_data


    def validate(self, data):
        user_obj = self.context.get('user_obj')
        business = data['i_business']
        my_favourite = models.MyFavourite.objects.filter(i_user=user_obj,i_business=business)
        if my_favourite:
            my_favourite.delete()
            status = {"deleted":True}
            return status
        else:
            return data

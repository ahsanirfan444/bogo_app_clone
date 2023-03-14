from rest_framework import serializers
from hubur_apis import models


class GetAllCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id','name','image',)

class CreateUserInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInterest
        fields = ('id','i_category','i_user',)
        extra_kwargs = {'i_user': {'read_only': True}}
    
    def validate(self, value):
        user_obj = self.context.get('user_obj')
        value['i_user'] = user_obj
        user_interest_obj = models.UserInterest.objects.filter(i_user=user_obj)
        if user_interest_obj:
            raise serializers.ValidationError("interest has already added for this user. Please update your interest")

        return super().validate(value)
    
class UpdateUserInterestSerializer(serializers.ModelSerializer):
    category = GetAllCategoriesSerializer(many=True, allow_null=True)
    class Meta:
        model = models.UserInterest
        fields = ('id','i_category','i_user','category',)
        extra_kwargs = {'i_user': {'read_only': True}}
    
    def validate(self, value):
        user_obj = self.context.get('user_obj')
        if value:
            value['category'] = value['i_category'] 
            value['i_user'] = user_obj
            
        return super().validate(value)

class GetUserInterestSerializer(serializers.ModelSerializer):
    i_category = GetAllCategoriesSerializer(many=True)
    class Meta:
        model = models.UserInterest
        fields = ('id','i_category','i_user' )
    
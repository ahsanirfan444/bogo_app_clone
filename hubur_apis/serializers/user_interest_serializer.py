from rest_framework import serializers
from hubur_apis import models


class GetAllCategoriesSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('context')
        super().__init__(*args, **kwargs)
        
        try:
            request = self.context.get('request')
            if request.user.is_authenticated:
                if request.user.lang_code == 1:
                    del self.fields['name_ar']
                else:
                    self.fields['name'] = self.fields['name_ar']

            else:
                if request.headers.get('Accept-Language') == str(1):
                    del self.fields['name_ar']
                else:
                    self.fields['name'] = self.fields['name_ar']

        except Exception as e:
            # print(e)
            pass

    class Meta:
        model = models.Category
        fields = ('id','name', 'name_ar', 'image',)

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

    class Meta:
        model = models.UserInterest
        fields = ('id','i_category','i_user' )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('context')
        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        i_category = instance.i_category
        data['i_category'] = GetAllCategoriesSerializer(i_category, context={'request': request}, many=True).data
        return data
    
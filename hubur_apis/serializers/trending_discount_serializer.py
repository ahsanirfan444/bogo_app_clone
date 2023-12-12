
from hubur_apis import models
from rest_framework import serializers


class TrendingDiscountSerializer(serializers.ModelSerializer):
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
        model = models.TrendingDiscount
        fields = ("id","name", "name_ar","image",)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return {k: v if v is not None else "" for k, v in response.items()}


class TrendingDiscountForCatagoriesSerializer(serializers.ModelSerializer):
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
        model = models.TrendingDiscount
        fields = ("id","name", "name_ar")

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return {k: v if v is not None else "" for k, v in response.items()}
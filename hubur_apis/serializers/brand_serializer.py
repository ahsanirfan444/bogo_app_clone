from hubur_apis import models
from rest_framework import serializers
from django.db.models import Q
from hubur_apis.serializers.content_serializer import ContentDetailSerializer

class HomeBrandListSerializer(serializers.ModelSerializer):
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
         model = models.Brand
         fields = ("id","image","name", "name_ar",)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['type'] = "brand"
        return {k: v if v is not None else "" for k, v in response.items()}

class BrandListSerializer(serializers.ModelSerializer):
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
         model = models.Brand
         fields = ("id","image","name", "name_ar", "website",)

    def to_representation(self, instance):
        request = self.context.get('request')
        products = models.Content.objects.filter(content_type=1, i_brand=instance).exclude(Q(i_brand__is_active=False) | Q(i_sub_category__is_active=False) | Q(i_business__i_user__is_active=False) | Q(is_active=False) | Q(i_business__is_active=False))
        product_serializer = ContentDetailSerializer(products, context={"request": request}, many=True)
        response = super().to_representation(instance)
        response['products'] = product_serializer.data
        response['type'] = "brand"
        return response
    
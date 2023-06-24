from hubur_apis import models
from rest_framework import serializers

from hubur_apis.serializers.content_serializer import ContentDetailSerializer

class HomeBrandListSerializer(serializers.ModelSerializer):

    class Meta:
         model = models.Brand
         fields = ("id","image","name",)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['type'] = "brand"
        return response

class BrandListSerializer(serializers.ModelSerializer):

    class Meta:
         model = models.Brand
         fields = ("id","image","name","website",)

    def to_representation(self, instance):
        products = models.Content.objects.filter(content_type=1, i_brand=instance)
        product_serializer = ContentDetailSerializer(products, many=True)
        response = super().to_representation(instance)
        response['products'] = product_serializer.data
        response['type'] = "brand"
        return response
    
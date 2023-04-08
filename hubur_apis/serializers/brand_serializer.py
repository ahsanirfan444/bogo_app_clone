from hubur_apis import models
from rest_framework import serializers

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
         fields = ("id","image","name","website",'founded_country','founded_year',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['products'] = []
        response['type'] = "brand"
        return response
    
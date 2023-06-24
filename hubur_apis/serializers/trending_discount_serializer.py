
from hubur_apis import models
from rest_framework import serializers


class TrendingDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TrendingDiscount
        fields = ("id","name","image",)


class TrendingDiscountForCatagoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TrendingDiscount
        fields = ("id","name",)
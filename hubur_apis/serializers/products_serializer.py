from rest_framework import serializers
from hubur_apis import models

class GetProductsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='i_sub_category.i_category.name')
    sub_category_name = serializers.CharField(source='i_sub_category.name')
    class Meta:
        model = models.Content
        fields = ('id','name', 'disc', 'picture', 'category_name','sub_category_name', 'price', )


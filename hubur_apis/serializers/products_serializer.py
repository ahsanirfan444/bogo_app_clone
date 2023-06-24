from rest_framework import serializers
from hubur_apis import models
from hubur_apis.serializers.search_serializer import GetSubCategorySerializer

class GetProductsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='i_sub_category.i_category.name')
    i_sub_category = GetSubCategorySerializer(many=True)
    class Meta:
        model = models.Content
        fields = ('id','name', 'description', 'picture', 'category_name','i_sub_category', 'price', )


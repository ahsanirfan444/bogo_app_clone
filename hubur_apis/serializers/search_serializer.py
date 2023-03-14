from rest_framework import serializers
from hubur_apis import models

class GetProductsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='i_sub_category.i_category.name')
    sub_category_name = serializers.CharField(source='i_sub_category.name')
    type = serializers.CharField(default='Product')
    class Meta:
        model = models.Content
        fields = ('name', 'disc', 'picture', 'category_name','sub_category_name', 'price','type', )


class GetBusinessSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='i_category.name')
    type = serializers.CharField(default='Business')
    class Meta:
        model = models.Business
        fields = ('name', 'contact', 'category_name', 'country_code', 'type',)


class GetBrandSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='Brand')
    class Meta:
        model = models.Brand
        fields = ('name', 'image', 'founded_year', 'founded_country', 'website', 'type',)


class GetSubCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='i_category.name')
    type = serializers.CharField(default='Sub Category')
    class Meta:
        model = models.SubCategories
        fields = ('name', 'category_name', 'type',)


class PopularSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PopularSearch
        fields = ('name', 'count','url',)
    
    def validate(self, validate_data):
        popular_search_data = models.PopularSearch.objects.filter(name=validate_data['name'])
        if popular_search_data:
            popular_search_data = popular_search_data.first()
            count = popular_search_data.count + 1
            popular_search_data.count = count
            popular_search_data.save()
            validate_data['count'] = count
            return super().validate(validate_data)
        else:
            return super().validate(validate_data)
        
class PopularSearchListSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(source="url")
    class Meta:
        model = models.PopularSearch
        fields = ('name','image_url',)
    
   
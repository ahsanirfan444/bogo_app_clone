from rest_framework import serializers
from hubur_apis import models

class GetSubCategorySerializer(serializers.ModelSerializer):
    i_category = serializers.CharField(source='i_category.name')
    class Meta:
        model = models.SubCategories
        fields = ('id','name', 'i_category',)


class SubCatagoriesListSerializer(serializers.ModelSerializer):
    i_category = serializers.CharField(source='i_category.name')
    class Meta:
        model = models.SubCategories
        fields = ('name','i_category',)


class GetProductsSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='Product')
    i_sub_category = SubCatagoriesListSerializer(many=True)
    class Meta:
        model = models.Content
        fields = ('id','name', 'picture','i_sub_category', 'type', )

    def to_representation(self, instance):
        response =super().to_representation(instance)
        response['image'] = response['picture']
        del response['picture']
        sub_cat_name_list = []
        cat_name = ''

        for cat_name in response['i_sub_category']:
            sub_cat_name_list.append(cat_name['name'])
            cat_name = cat_name['i_category']

        response['i_sub_category'] = sub_cat_name_list
        response['i_category'] = cat_name
        return response


class GetBusinessSerializer(serializers.ModelSerializer):
    i_category = serializers.CharField(source='i_category.name')
    type = serializers.CharField(default='Business')
    i_subcategory = SubCatagoriesListSerializer(many=True)
    class Meta:
        model = models.Business
        fields = ('id','name', 'i_category','i_subcategory', 'type','logo_pic',)

    def to_representation(self, instance):
        response =super().to_representation(instance)
        response['image'] = response['logo_pic']
        name_list = []
        for name in response['i_subcategory']:
            name_list.append(name['name'])
        response['i_sub_category'] = name_list
        del response['logo_pic'],response['i_subcategory']
        return response


class GetBrandSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='Brand')
    class Meta:
        model = models.Brand
        fields = ('id','name', 'image', 'type',)

    def to_representation(self, instance):
        response =super().to_representation(instance)
        response['i_sub_category'] = []
        response['i_category'] = ""
        return response


class SearchSerializer(serializers.Serializer):
    class Meta:
        fields = ('image', 'picture','logo_pic','type_id','type',)
    
    def to_representation(self, instance):
        response =  super().to_representation(instance)

        if 'picture' in response:
            response['image'] = response['picture']
            del response['picture']

        if 'logo_pic' in response:
            response['image'] = response['logo_pic']
            del response['logo_pic']
    
        return response
          

class PopularSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PopularSearch
        fields = ('name', 'count','url','type_id','type','catagory',)

    
    def validate(self, validate_data):
        popular_search_data = models.PopularSearch.objects.filter(type=validate_data['type'], type_id=validate_data['type_id'])
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
        fields = ('name','image_url','type','type_id','catagory',)
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['id'] = response['type_id']
        del response['type_id']
        return response
    

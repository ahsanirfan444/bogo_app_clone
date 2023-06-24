from rest_framework import serializers
from hubur_apis import models
from hubur_apis.serializers.brand_serializer import BrandListSerializer
from hubur_apis.serializers.content_serializer import ProductImagesListSerializer

class GetSubCategorySerializer(serializers.ModelSerializer):
    i_category = serializers.CharField(source='i_category.name')
    class Meta:
        model = models.SubCategories
        fields = ('id','name', 'i_category','image',)
    
    def to_representation(self, instance):
        response =  super().to_representation(instance)
        sub_cat_list_for_filter = self.context.get('sub_cat_list_for_filter')
        if sub_cat_list_for_filter and sub_cat_list_for_filter == True:
            del response['i_category'], response['image']
        return response

class SubCatagoriesListSerializer(serializers.ModelSerializer):
    i_category = serializers.CharField(source='i_category.name')
    class Meta:
        model = models.SubCategories
        fields = ('name','i_category',)


class GetProductsSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField("get_content_type")
    i_sub_category = serializers.CharField(source="i_sub_category.name")
    i_category = serializers.CharField(source="i_sub_category.i_category.name")
    class Meta:
        model = models.Content
        fields = ('id','name','content_type','i_category', 'i_sub_category',)

    def to_representation(self, instance):
        response =super().to_representation(instance)

        content_image = models.Images.objects.filter(i_content=instance).last()

        content_image = ProductImagesListSerializer(content_image).data
        response['image'] = content_image['image']
        response['type'] = response['content_type']
        response['i_sub_category'] = [response['i_sub_category']]
        del response['content_type']
        
        return response
    
    def get_content_type(self,value):
        return value.get_content_type_display()


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
    obj_id = serializers.IntegerField()
    class Meta:
        model = models.PopularSearch
        fields = ('i_brand', 'i_business', 'i_content', 'count','type','obj_id',)

    
    def validate(self, validate_data):
        if validate_data['type'] == "Business":
        
            popular_search_data = models.PopularSearch.objects.filter(type=validate_data['type'], i_business_id=validate_data['obj_id'])

        elif validate_data['type'] == "Brand":
        
            popular_search_data = models.PopularSearch.objects.filter(type=validate_data['type'], i_brand_id=validate_data['obj_id'])
        
        elif validate_data['type'] == "Content":
        
            popular_search_data = models.PopularSearch.objects.filter(type=validate_data['type'], i_content_id=validate_data['obj_id'])
        else:
            raise serializers.ValidationError("Not valid type")
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
    business_name = serializers.CharField(source="i_business.name",default="")
    brand_name = serializers.CharField(source="i_brand.name",default="")
    content_name = serializers.CharField(source="i_content.name",default="")
    catagory = serializers.CharField(source="i_business.i_category.name",default="")
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = models.PopularSearch
        fields = ('i_brand','i_business','i_content','type','business_name','brand_name','content_name','catagory','image_url',)
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        if response['i_brand']:
            response['id'] = response['i_brand']
            response['name'] = response['brand_name']
            del response['i_brand'],response['brand_name'],response['business_name'],response['i_business'],response['i_content'],response['content_name']
        
        elif response['i_business']:
            response['id'] = response['i_business']
            response['name'] = response['business_name']
            del response['i_business'],response['business_name'],response['brand_name'],response['i_brand'],response['i_content'],response['content_name']

        elif response['i_content']:
            response['id'] = response['i_content']
            response['name'] = response['content_name']
            del response['i_content'],response['content_name'], response['i_business'],response['business_name'],response['brand_name'],response['i_brand']

        return response
    
    def get_image_url(self,obj):
        if obj.i_business:
            image_url = GetBusinessSerializer(obj.i_business)
            image_url = image_url.data['image']
        elif obj.i_content:
            images = models.Images.objects.filter(is_active=True,i_content=obj.i_content).order_by('-created_at').first()
            image_url =(ProductImagesListSerializer(images)).data['image']
        else:
            image_url = BrandListSerializer(obj.i_brand)
            image_url = image_url.data['image']
        return image_url


class SubCatagoryBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Banner
        fields = ('image','url',)
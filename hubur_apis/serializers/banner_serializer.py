from hubur_apis import models
from rest_framework import serializers
import global_methods

class BannerListSerializer(serializers.ModelSerializer):
    class Meta:
         model = models.Banner
         fields = ("id","image","position",)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('context')
        super().__init__(*args, **kwargs)

    def get_full_url(self):
        request = self.context.get('request')
        url = models.Banner.image.url
        return request.build_absolute_uri(url)


class SubCatListSerializer(serializers.ModelSerializer):
    class Meta:
        model= models.SubCategories
        fields = ("id","name",)


class HomeBusinessSerializer(serializers.ModelSerializer):
    catagory = serializers.CharField(source="i_category.name")
    i_subcategory = SubCatListSerializer(many=True)
    total_distance = serializers.CharField(required=False)

    class Meta:
         model = models.Business
         fields = ("id","name","contact","country_code","address","long","lat","website","logo_pic","catagory","i_subcategory","is_claimed","place_id",'total_distance')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('context')
        super().__init__(*args, **kwargs)

    def get_full_url(self):
        request = self.context.get('request')
        url = models.Business.logo_pic.url
        return request.build_absolute_uri(url)
    
    def to_representation(self, data):
        business_long= data.long
        business_lat= data.lat
        request = self.context.get('request')
        user_id = request.user.id
        response = super().to_representation(data)
        if user_id != None:
            user_long = request.user.long
            user_lat = request.user.lat
            if user_long and user_lat != None:
                total_distance = global_methods.distance(business_lat,business_long,user_lat,user_long)
                response['total_distance'] = total_distance
        if data.is_claimed == 2:
            response['is_claimed'] = True
        else:
            response['is_claimed'] = False
        return response
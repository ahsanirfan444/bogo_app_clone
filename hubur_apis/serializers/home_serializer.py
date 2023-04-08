
from rest_framework import serializers
from global_methods import distance
from hubur_apis import models
from hubur_apis.serializers.banner_serializer import SubCatListSerializer
from hubur_apis.serializers.entity_details_serializer import GalleryImagesListSerializer


class HomeBusinessSerializer(serializers.ModelSerializer):
    catagory = serializers.CharField(source="i_category.name")
    i_subcategory = SubCatListSerializer(many=True)

    class Meta:
         model = models.Business
         fields = ("id","name","logo_pic","catagory","i_subcategory",)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('context')
        super().__init__(*args, **kwargs)

    def get_full_url(self):
        request = self.context.get('request')
        url = models.Business.logo_pic.url
        return request.build_absolute_uri(url)
    
    def to_representation(self, data):
        response = super().to_representation(data)

        name_list = []
        for name in response['i_subcategory']:
            name_list.append(name['name'])
        response['i_sub_category'] = name_list
        del response['i_subcategory']
        gallery_images_list = []
        gallery_images = models.Images.objects.filter(i_business=data, is_active=True)
        if gallery_images:
            gallery_images = GalleryImagesListSerializer(gallery_images,many=True)
            for images in gallery_images.data:
                gallery_images_list.append(images['image'])

        response['gallery_images'] = gallery_images_list
        return response
    

class HomeBusinessWithAddressSerializer(serializers.ModelSerializer):
    catagory = serializers.CharField(source="i_category.name")
    i_subcategory = SubCatListSerializer(many=True)

    class Meta:
         model = models.Business
         fields = ("id","name","address","logo_pic","catagory","i_subcategory",)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('context')
        super().__init__(*args, **kwargs)

    def get_full_url(self):
        request = self.context.get('request')
        url = models.Business.logo_pic.url
        return request.build_absolute_uri(url)
    
    def to_representation(self, data):
        response = super().to_representation(data)

        name_list = []
        for name in response['i_subcategory']:
            name_list.append(name['name'])
        response['i_sub_category'] = name_list
        del response['i_subcategory']

        gallery_images_list = []
        gallery_images = models.Images.objects.filter(i_business=data, is_active=True)
        if gallery_images:
            gallery_images = GalleryImagesListSerializer(gallery_images,many=True)
            for images in gallery_images.data:
                gallery_images_list.append(images['image'])

        response['gallery_images'] = gallery_images_list

        return response


class NearByDealsSerializer(serializers.ModelSerializer):
    catagory = serializers.CharField(source="i_category.name")
    i_subcategory = SubCatListSerializer(many=True)

    class Meta:
         model = models.Business
         fields = ("id","name","address","logo_pic","catagory","i_subcategory",)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('context')
        super().__init__(*args, **kwargs)

    def get_full_url(self):
        request = self.context.get('request')
        url = models.Business.logo_pic.url
        return request.build_absolute_uri(url)
    
    def to_representation(self, data):
        response = super().to_representation(data)

        name_list = []
        for name in response['i_subcategory']:
            name_list.append(name['name'])
        response['i_sub_category'] = name_list
        del response['i_subcategory']
        gallery_images_list = []
        gallery_images = models.Images.objects.filter(i_business=data, is_active=True)
        if gallery_images:
            gallery_images = GalleryImagesListSerializer(gallery_images,many=True)
            for images in gallery_images.data:
                gallery_images_list.append(images['image'])

        response['gallery_images'] = gallery_images_list


        user_long = self.context.get('user_long')
        user_lat = self.context.get('user_lat')
    
        total_distance = distance(user_long,user_lat,data.long,data.lat)
        if float(total_distance) <= 10:
            return response
        
        
class LocationForGuestModeSerializer(serializers.Serializer):
    long = serializers.FloatField()
    lat = serializers.FloatField()

    class Meta:
         fields = ("long","lat",)
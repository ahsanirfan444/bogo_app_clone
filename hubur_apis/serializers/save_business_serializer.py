from hubur_apis import models
from hubur_apis.serializers.banner_serializer import SubCatListSerializer
from hubur_apis.serializers.entity_details_serializer import GalleryImagesListSerializer
from rest_framework import serializers


class VisitedBusinessSerializer(serializers.ModelSerializer):
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
        gallery_images = models.Images.objects.filter(i_business=data, is_active=True, type=1)
        if gallery_images:
            gallery_images = GalleryImagesListSerializer(gallery_images,many=True)
            for images in gallery_images.data:
                gallery_images_list.append(images['image'])

        response['gallery_images'] = gallery_images_list

        user_obj = self.context.get('user_obj')

        fav_obj = models.MyFavourite.objects.filter(i_user=user_obj, i_business=data)
        if fav_obj:
            fav_obj = True
        else:
            fav_obj = False
        
        response['my_favourite'] = fav_obj

        return response
    
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



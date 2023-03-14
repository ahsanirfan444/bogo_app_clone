from hubur_apis import models
from rest_framework import serializers

class BrandListSerializer(serializers.ModelSerializer):

    class Meta:
         model = models.Brand
         fields = ("id","image","name","website",)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('context')
        super().__init__(*args, **kwargs)

    def get_full_url(self):
        request = self.context.get('request')
        url = models.Brand.logo.url
        return request.build_absolute_uri(url)
    
from hubur_apis import models
from rest_framework import serializers
import global_methods

class BannerListSerializer(serializers.ModelSerializer):
    platform = serializers.SerializerMethodField("get_platform")
    class Meta:
         model = models.Banner
         fields = ("id","image","position","url","platform",)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('context')
        super().__init__(*args, **kwargs)

    def get_full_url(self):
        request = self.context.get('request')
        url = models.Banner.image.url
        return request.build_absolute_uri(url)
    
    def get_platform(self,value):
        return value.get_platform_display()


class SubCatListSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('context')
        super().__init__(*args, **kwargs)
        
        try:
            request = self.context.get('request')
            if request.user.is_authenticated:
                if request.user.lang_code == 1:
                    del self.fields['name_ar']
                else:
                    self.fields['name'] = self.fields['name_ar']

            else:
                if request.headers.get('Accept-Language') == str(1):
                    del self.fields['name_ar']
                else:
                    self.fields['name'] = self.fields['name_ar']

        except Exception as e:
            # print(e)
            pass

    class Meta:
        model= models.SubCategories
        fields = ("id","name", "name_ar",)



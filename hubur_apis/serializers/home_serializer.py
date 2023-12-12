
from rest_framework import serializers
from global_methods import distance
from hubur_apis import models
from hubur_apis.serializers.banner_serializer import SubCatListSerializer
from hubur_apis.serializers.content_serializer import ShowOfferOnBusinessSerializer
from hubur_apis.serializers.entity_details_serializer import GalleryImagesListSerializer
from hubur_apis.serializers.review_serializer import AggregateBusinessReviewsSerializer
from django.db.models import Count

class HomeBusinessSerializer(serializers.ModelSerializer):
    catagory = serializers.CharField(source="i_category.name")
    # i_subcategory = SubCatListSerializer(many=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('context')
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.Business
        fields = ("id","name","logo_pic","catagory", "i_subcategory", "is_featured")

    def get_full_url(self):
        request = self.context.get('request')
        url = models.Business.logo_pic.url
        return request.build_absolute_uri(url)
    
    def to_representation(self, data):
        response = super().to_representation(data)

        request = self.context.get('request')
        i_subcategory = data.i_subcategory
        response['i_subcategory'] = SubCatListSerializer(i_subcategory, context={'request': request}, many=True).data

        name_list = []
        for name in response['i_subcategory']:
            name_list.append(name['name'] if name['name'] is not None else "")
        response['i_sub_category'] = name_list
        del response['i_subcategory']

        rating = AggregateBusinessReviewsSerializer(data).data
        response['average_rate'] = rating['average_rate']
        response['total_reviews'] = rating['total_reviews']
        
        gallery_images_list = []
        gallery_images = models.Images.objects.filter(i_business=data, is_active=True, type=1)
        if gallery_images:
            gallery_images = GalleryImagesListSerializer(gallery_images,many=True)
            for images in gallery_images.data:
                gallery_images_list.append(images['image'])

        response['gallery_images'] = gallery_images_list
        return response
    

class HomeBusinessWithAddressSerializer(serializers.ModelSerializer):
    catagory = serializers.CharField(source="i_category.name")
    # i_subcategory = SubCatListSerializer(many=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('context')
        super().__init__(*args, **kwargs)

    class Meta:
         model = models.Business
         fields = ("id","name","address","logo_pic","catagory", "i_subcategory", "is_featured")

    def get_full_url(self):
        request = self.context.get('request')
        url = models.Business.logo_pic.url
        return request.build_absolute_uri(url)
    
    def to_representation(self, data):
        response = super().to_representation(data)

        request = self.context.get('request')
        i_subcategory = data.i_subcategory
        response['i_subcategory'] = SubCatListSerializer(i_subcategory, context={'request': request}, many=True).data

        name_list = []
        for name in response['i_subcategory']:
            name_list.append(name['name'] if name['name'] is not None else "")
        response['i_sub_category'] = name_list
        del response['i_subcategory']

        rating = AggregateBusinessReviewsSerializer(data).data
        response['average_rate'] = rating['average_rate']
        response['total_reviews'] = rating['total_reviews']

        gallery_images_list = []
        gallery_images = models.Images.objects.filter(i_business=data, is_active=True, type=1)
        if gallery_images:
            gallery_images = GalleryImagesListSerializer(gallery_images,many=True)
            for images in gallery_images.data:
                gallery_images_list.append(images['image'])

        response['gallery_images'] = gallery_images_list

        all_business_content = models.Content.objects.filter(i_business=data, is_active=True)
        redeemed_content = models.Redemption.objects.filter(i_content__in=list(all_business_content), is_redeemed=True).values('i_content').annotate(count=Count('i_content')).order_by('-count')
        if redeemed_content:
            for content in redeemed_content:
                most_redeemed_content =  content['i_content'] 
                offer = models.Offers.objects.filter(i_content=most_redeemed_content, is_active=True).first()
                offer_data = ShowOfferOnBusinessSerializer(offer, context={"request": request, "content": most_redeemed_content}).data
                response['offer'] = offer_data
                if offer:
                    break
                else:
                    try:
                        offer = models.Offers.objects.filter(i_business=data, is_active=True).first()
                        offer_data = ShowOfferOnBusinessSerializer(offer, context={"request": request, "content": offer.i_content.filter(is_active=True).first().id}).data
                        response['offer'] = offer_data
                    except Exception as e:
                        # print(e)
                        response['offer'] = None
        
        else:
            try:
                offer = models.Offers.objects.filter(i_business=data, is_active=True).first()
                offer_data = ShowOfferOnBusinessSerializer(offer, context={"request": request, "content": offer.i_content.filter(is_active=True).first().id}).data
                response['offer'] = offer_data
            except Exception as e:
                # print(e)
                response['offer'] = None

        return response


class NearByDealsSerializer(serializers.ModelSerializer):
    catagory = serializers.CharField(source="i_category.name")
    catagory_ar = serializers.CharField(source="i_category.name_ar")
    # i_subcategory = SubCatListSerializer(many=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('context')
        super().__init__(*args, **kwargs)
        
        try:
            request = self.context.get('request')
            if request.user.is_authenticated:
                if request.user.lang_code == 1:
                    del self.fields['catagory_ar']
                else:
                    self.fields['catagory'] = self.fields['catagory_ar']

            else:
                if request.headers.get('Accept-Language') == str(1):
                    del self.fields['catagory_ar']
                else:
                    self.fields['catagory'] = self.fields['catagory_ar']

        except Exception as e:
            # print(e)
            pass

    class Meta:
         model = models.Business
         fields = ("id","name","address","logo_pic","catagory", "catagory_ar", "i_subcategory", "is_featured")

    def get_full_url(self):
        request = self.context.get('request')
        url = models.Business.logo_pic.url
        return request.build_absolute_uri(url)
    
    def to_representation(self, data):
        response = super().to_representation(data)

        request = self.context.get('request')
        i_subcategory = data.i_subcategory
        response['i_subcategory'] = SubCatListSerializer(i_subcategory, context={'request': request}, many=True).data

        name_list = []
        for name in response['i_subcategory']:
            name_list.append(name['name'] if name['name'] is not None else "")
        response['i_sub_category'] = name_list
        del response['i_subcategory']
        gallery_images_list = []
        gallery_images = models.Images.objects.filter(i_business=data, is_active=True, type=1)

        rating = AggregateBusinessReviewsSerializer(data).data
        response['average_rate'] = rating['average_rate']
        response['total_reviews'] = rating['total_reviews']
        
        if gallery_images:
            gallery_images = GalleryImagesListSerializer(gallery_images,many=True)
            for images in gallery_images.data:
                gallery_images_list.append(images['image'])

        response['gallery_images'] = gallery_images_list

        all_business_content = models.Content.objects.filter(i_business=data)
        redeemed_content = models.Redemption.objects.filter(i_content__in=list(all_business_content), is_redeemed=True).values('i_content').annotate(count=Count('i_content')).order_by('-count')
        try:
            most_redeemed_content = list(redeemed_content)[0]['i_content']
            offer = models.Offers.objects.get(i_content=most_redeemed_content)
            offer_data = ShowOfferOnBusinessSerializer(offer, context={"request": request, "content": most_redeemed_content}).data
            response['offer'] = offer_data
        except Exception as e:
            # print(e)
            response['offer'] = None


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
from hubur_apis import models
from rest_framework import serializers
import global_methods
from hubur_apis.serializers.business_serializer import BusinessSerializerForTimeOnly
from hubur_apis.serializers.content_serializer import ContentDetailSerializer
from hubur_apis.serializers.offer_serializer import OffersListSerializer
from hubur_apis.serializers.review_serializer import AggregateBusinessReviewsSerializer, GetAllReviewsSerializer
from hubur_apis.serializers.search_serializer import SubCatagoriesListSerializer
from global_methods import format_number
from datetime import datetime
now = datetime.now()
from django.db.models import Q

class StoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Story
        fields = ('image','video',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return_data = {key: value for key, value in data.items() if value is not None}
        return list(return_data.values())[0]

class GalleryImagesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Images
        fields = ("id","image",)

class BusinessListSerializer(serializers.ModelSerializer):
    i_category = serializers.CharField(source="i_category.name")
    vendor_id = serializers.IntegerField(source='i_user.id',default=0)
    i_subcategory = SubCatagoriesListSerializer(many=True)
    business_time = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField("get_i_attributes")
    class Meta:
        model = models.Business
        fields = ("id","vendor_id","name","country_code","about","attributes","contact","address","long","lat","website","logo_pic","i_category","i_subcategory","is_claimed","place_id","business_time", "is_featured")

    def get_business_time(self,obj):
        request = self.context.get('request')
        status = (BusinessSerializerForTimeOnly(obj, context={"request": request})).data
        return status
    
    def get_i_attributes(self,obj):
        if obj.i_category == 'Restaurant':
            attributes = obj.i_attributes.all().values_list('name',flat=True)
            return attributes
        else:
            return []
    
    def to_representation(self, data):
        request = self.context.get('request')
        business_long= data.long
        business_lat= data.lat

        if 'user_lat' and 'user_long' in self.context:

            guest_user_lat = self.context['user_lat']
            guest_user_long = self.context['user_long']

            response = super().to_representation(data)
            total_distance = global_methods.distance(business_lat,business_long,guest_user_lat,guest_user_long)
            response['total_distance'] = total_distance
            response['is_redeemed'] = False
        else:
            if request:
                user_id = request.user.id
                response = super().to_representation(data)
        
            all_products = models.Content.objects.filter(i_business=data, is_active=True, i_sub_category__is_active=True).exclude(i_brand__is_active=False)[:8]

            if user_id != None:
                user_long = request.user.long
                user_lat = request.user.lat
                voting_obj =models.Voting.objects.filter(i_business=data, i_user_id=user_id)
                if voting_obj:
                    voting_obj = voting_obj.first()
                    response['vote'] = voting_obj.vote
                else:
                    response['vote'] = ""
                
                my_fav_obj =models.MyFavourite.objects.filter(i_business=data, i_user_id=user_id)
                if my_fav_obj:
                    my_fav_obj = my_fav_obj.first()
                    response['my_favourite'] = True
                else:
                    response['my_favourite'] = False

                my_bookmark_obj =models.MyBookmark.objects.filter(i_business=data, i_user_id=user_id)
                if my_bookmark_obj:
                    my_bookmark_obj = my_bookmark_obj.first()
                    response['my_bookmark'] = True
                else:
                    response['my_bookmark'] = False
                
                
                context = {"user_obj":request.user, "request": request}
                response['products'] = (ContentDetailSerializer(all_products, context=context, many=True)).data


                if user_long and user_lat != None:
                    total_distance = global_methods.distance(business_lat,business_long,user_lat,user_long)
                    response['total_distance'] = total_distance
                    redeemed_ob = models.Redemption.objects.filter(created_at__date = now.date(), i_user=request.user, i_content__i_business_id =data.id)
                    if redeemed_ob:
                        response['is_redeemed'] = True
                    else:
                        response['is_redeemed'] = False
                else:
                    response['total_distance'] = ""
                    response['is_redeemed'] = False
            else:
                context = {"request": request}
                response['products'] = (ContentDetailSerializer(all_products, context=context, many=True)).data
                response['total_distance'] = ""
                response['is_redeemed'] = False

        if data.is_claimed == 2:
            response['is_claimed'] = True
        else:
            response['is_claimed'] = False
        name_list = []
        for name in response['i_subcategory']:
            name_list.append(name['name'])
        response['i_sub_category'] = name_list
        response['image'] = response['logo_pic']
        del response['logo_pic'], response['i_subcategory']
        response['reviews'] = []
        response['rating'] = ""

        dict1 = dict(response)
        dict2 = dict(response['business_time'])
        response = {**dict2, **dict1}
        del response['business_time']
        
        stories_objs = models.Story.objects.filter(is_active=True, i_user__is_active=True, i_business_id=data.id).order_by('-created_at')[:10]
        story_serializer = StoryListSerializer(stories_objs, many=True)
        response['checkin_storys'] = story_serializer.data

        gallery_images_list = []
        gallery_images = models.Images.objects.filter(i_business=data, is_active=True, type=1)
        if gallery_images:
            gallery_images = GalleryImagesListSerializer(gallery_images,many=True)
            for images in gallery_images.data:
                gallery_images_list.append(images['image'])

        response['gallery_images'] = gallery_images_list

        response['rating'] = AggregateBusinessReviewsSerializer(data).data

        all_reviews = models.Reviews.objects.filter(i_business=data.id)[:5]

        response['reviews'] = GetAllReviewsSerializer(all_reviews, many=True).data


        total_checkins = models.Checkedin.objects.filter(i_business=data).exclude(i_user__is_active=False).count()
        total_checkins = format_number(total_checkins)
        response['checkins'] = total_checkins


        response['place_id'] = 'https://www.google.com/maps/place/?q=place_id:'+response['place_id']

        offers = models.Offers.objects.filter(i_business=data.id, is_active=True, is_expiry=False)
        hot_offers = OffersListSerializer(offers, context={"request": request}).data['hot_offers']
        daily_offers = OffersListSerializer(offers, context={"request": request}).data['daily_offers']
        weekly_offers = list(OffersListSerializer(offers, context={"request": request}).data['weekly_offers'])
        monthly_offers = list(OffersListSerializer(offers, context={"request": request}).data['monthly_offers'])
        response['offers'] = [hot_offers,daily_offers, weekly_offers, monthly_offers]
        
        return response
    


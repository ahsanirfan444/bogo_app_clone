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

class CheckinStoryListSerializer(serializers.ModelSerializer):
    checkin_story_image = serializers.ImageField(source="i_story.image")
    checkin_story_video = serializers.ImageField(source="i_story.video")
    class Meta:
        model = models.Checkedin
        fields = ('checkin_story_image','checkin_story_video')
   

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
        fields = ("id","vendor_id","name","country_code","about","attributes","contact","address","long","lat","website","logo_pic","i_category","i_subcategory","is_claimed","place_id","business_time",)

    def get_business_time(self,obj):
        status = (BusinessSerializerForTimeOnly(obj)).data
        return status
    
    def get_i_attributes(self,obj):
        if obj.i_category == 'Restaurant':
            attributes = obj.i_attributes.all().values_list('name',flat=True)
            return attributes
        else:
            return []
    
    def to_representation(self, data):

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
            request = self.context.get('request')
            if request:
                user_id = request.user.id
                response = super().to_representation(data)
        
            all_products = models.Content.objects.filter(i_business=data, is_active=True)[:8]

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
                
                
                context = {"user_obj":request.user}
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
                response['products'] = (ContentDetailSerializer(all_products, many=True)).data
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
        
        checkin_storys_obj = models.Checkedin.objects.filter(i_business_id=data.id, i_story__is_active = True).exclude(i_story__video = None)
        checkin_storys_serializer = CheckinStoryListSerializer(checkin_storys_obj,many=True)
        if checkin_storys_serializer:
            checkin_storys_list = []
            for i in checkin_storys_serializer.data:
                if i['checkin_story_image'] is not None:
                    checkin_storys_list.append(i['checkin_story_image'])
                else:
                    checkin_storys_list.append(i['checkin_story_video'])
            response['checkin_storys'] = checkin_storys_list
        else:
            response['checkin_storys'] = []

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


        total_checkins = models.Checkedin.objects.filter(i_business=data).count()
        total_checkins = format_number(total_checkins)
        response['checkins'] = total_checkins


        response['place_id'] = 'https://www.google.com/maps/place/?q=place_id:'+response['place_id']

        offers = models.Offers.objects.filter(i_business=data.id, is_active=True, is_expiry=False)
        hot_offers = OffersListSerializer(offers).data['hot_offers']
        daily_offers = OffersListSerializer(offers).data['daily_offers']
        weekly_offers = list(OffersListSerializer(offers).data['weekly_offers'])
        monthly_offers = list(OffersListSerializer(offers).data['monthly_offers'])
        response['offers'] = [hot_offers,daily_offers, weekly_offers, monthly_offers]
        
        return response
    


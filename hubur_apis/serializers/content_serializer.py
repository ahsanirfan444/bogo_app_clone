from rest_framework import serializers
from hubur_apis import models
from hubur_apis.serializers.business_serializer import BusinessSerializerForTimeOnly
from hubur_apis.serializers.review_serializer import AggregateReviewsSerializer, GetAllReviewsSerializer,AggregateBusinessReviewsSerializer
from datetime import datetime

from hubur_apis.serializers.story_serializer import BusinessLogoSerializer

class ProductImagesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Images
        fields = ("image",)

class OfferSerializer(serializers.ModelSerializer):
    offer_type_name = serializers.SerializerMethodField("get_type")
    offer_type = serializers.IntegerField(source="type")
    discount_type = serializers.SerializerMethodField("get_discount_type")
    discounted_price = serializers.SerializerMethodField()
    class Meta:
        model = models.Offers
        fields = ('offer_type_name','offer_type','discount_price','end','discount_type','discounted_price','is_expiry',)
    
    def get_type(self,obj):
        return obj.get_type_display()
    
    def get_discount_type(self,obj):
        return obj.get_discount_type_display()
    
    def get_discounted_price(self,obj):
        price = self.context.get('price')
        if price:
            discount_type = obj.discount_type
            if discount_type == 2:
                return price - obj.discount_price
            elif discount_type == 1:
                discount_price_in_percent = price * obj.discount_price/100
                return price - discount_price_in_percent

        return None
    
class ContentDetailSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField("get_content_type")
    business_time = serializers.SerializerMethodField()
    business_logo = serializers.SerializerMethodField()
    business_id = serializers.IntegerField(source='i_business.id')
    vendor_id = serializers.IntegerField(source='i_business.i_user.id',default=0)
    business_name = serializers.CharField(source='i_business.name')
    business_address = serializers.CharField(source='i_business.address')
    brand_id = serializers.IntegerField(source='i_brand.id', default=None)
    brand_name = serializers.CharField(source='i_brand.name', default=None)
    
    class Meta:
        model = models.Content
        fields = ("id","name","description","content_type","price","sku","color","code","quantity","business_id","vendor_id","business_name","business_address","business_time","business_logo","brand_id","brand_name",)

    def get_business_time(self,obj):
        business_obj = obj.i_business
        status = (BusinessSerializerForTimeOnly(business_obj)).data
        del status['id']
        return status
    
    def get_business_logo(self, obj):
        logo_pic = BusinessLogoSerializer(obj.i_business).data['logo_pic']
        return logo_pic
    
    def get_content_type(self,obj):
        return obj.get_content_type_display()
    
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        if 'user_obj' in self.context:
            user_obj = self.context.get("user_obj")
        else:
            user_obj = None

        if response['content_type'] == "Product":
            del response['code']
        elif response['content_type'] == "Service" or "Health Care" or "Menu":
            del response['sku'], response['color'], response['quantity']
        else:
            del response['sku'], response['color'], response['code'], response['quantity']

        dict1 = dict(response)
        dict2 = dict(response['business_time'])
        response = {**dict2, **dict1}
        del response['business_time']
        if user_obj:
        
            my_saved_offer_obj = models.SavedOffers.objects.filter(i_content=instance, i_user=user_obj)
            
            content_redeem = models.Redemption.objects.filter(i_content=instance, i_user=user_obj, created_at__date=datetime.now().date()).first()
            if my_saved_offer_obj:
                my_saved_offer_obj = my_saved_offer_obj.first()
                response['saved_offer'] = True
            else:
                response['saved_offer'] = False
            if content_redeem:
                response['is_redeem'] = True
            else:
                response['is_redeem'] = False
        else:
            response['saved_offer'] = False
            response['is_redeem'] = False

        offers = models.Offers.objects.filter(i_content=instance, is_active=True, is_expiry=False).first()
        context = {'price': instance.price}
        serializer = OfferSerializer(offers, context=context)
        if serializer.data['discount_price']:
            dict1 = dict(response)
            dict2 = dict(serializer.data)
            response = {**dict2, **dict1}
        else:
            response['is_expiry'] = True
            response['ofter_name'] = None
            response['ofter_type'] = None
            response['discount_price'] = None
            response['end'] = None
            response['discount_type'] = None
            response['discounted_price'] = None
        
        content_detail = self.context.get('content_detail')
        if content_detail:
            images = models.Images.objects.filter(is_active=True,i_content=instance).order_by('-created_at')
            list_of_images= (ProductImagesListSerializer(images, many=True)).data
            response['image']= [d['image'] for d in list_of_images]

        else:
            images = models.Images.objects.filter(is_active=True,i_content=instance).order_by('-created_at').first()
            response['image']= (ProductImagesListSerializer(images)).data['image']

        response['rating'] = AggregateReviewsSerializer(instance).data

        all_reviews = models.Reviews.objects.filter(i_content=instance.id)[:5]

        response['reviews'] = GetAllReviewsSerializer(all_reviews, many=True).data

        business_reviews_obj = AggregateBusinessReviewsSerializer(instance.i_business).data

        response['business_total_reviews'] = business_reviews_obj['total_reviews']
        response['business_average_rate'] = business_reviews_obj['average_rate']

        return response
    
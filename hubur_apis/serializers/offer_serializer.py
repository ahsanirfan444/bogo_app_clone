from global_methods import getCurrentLanguageContextForAppUsers, keyvalue
from hubur_apis import models
from rest_framework import serializers
from datetime import datetime, timezone
from django.db.models import Q

from hubur_apis.serializers.content_serializer import (
    ContentDetailSerializer,
    )
class OfferDetailSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField("get_type")
    class Meta:
        model = models.Offers
        fields = ('name','type')
    
    def get_type(self,obj):
        request = self.context.get('request')
        lang_obj = getCurrentLanguageContextForAppUsers(request)
        name = keyvalue(lang_obj, obj.get_type_display())
        return name
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context.get('request')
        i_content = instance.i_content
        i_content = i_content.filter(i_sub_category__is_active=True, is_active=True, i_business__is_active=True).exclude(Q(i_brand__is_active=False) | Q(i_business__i_user__is_active=False))
        content = ContentDetailSerializer(i_content, context={"request": request}, many=True).data
        response['result'] = content
        del response['name']
        return response

class BusinessOffersDetailSerializer(serializers.ModelSerializer):
    discount_type = serializers.SerializerMethodField("get_discount_type")
    business_id = serializers.IntegerField(source='i_business.id')
    business_name = serializers.CharField(source='i_business.name')
    offer_type_name = serializers.SerializerMethodField("get_type")
    offer_type = serializers.IntegerField(source="type")

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
        model = models.Offers
        fields = ('id','name', 'name_ar', 'image', 'discount_type','discount_price','end','business_id','business_name','offer_type_name','offer_type',)

    def get_discount_type(self,obj):
        return obj.get_discount_type_display()
    
    def get_type(self,obj):
        request = self.context.get('request')
        lang_obj = getCurrentLanguageContextForAppUsers(request)
        name = keyvalue(lang_obj, obj.get_type_display())
        return name

    
class OffersListSerializer(serializers.ModelSerializer):
    hot_offers = serializers.SerializerMethodField()
    daily_offers = serializers.SerializerMethodField()
    weekly_offers = serializers.SerializerMethodField()
    monthly_offers = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Offers
        fields = ("hot_offers","daily_offers","weekly_offers","monthly_offers",)

    def get_hot_offers(self, obj):
        request = self.context.get('request')
        hot_offers = obj.filter(type=4)
        hot_offers = BusinessOffersDetailSerializer(hot_offers, context={"request": request}, many=True).data[:4]
        return hot_offers
    
    def get_daily_offers(self, obj):
        request = self.context.get('request')
        daily_offers = obj.filter(type=1)
        daily_offers = BusinessOffersDetailSerializer(daily_offers, context={"request": request}, many=True).data[:4]
        return daily_offers

    def get_weekly_offers(self, obj):
        request = self.context.get('request')
        weekly_offers = obj.filter(type=2)
        weekly_offers = BusinessOffersDetailSerializer(weekly_offers, context={"request": request}, many=True).data[:4]
        return weekly_offers

    def get_monthly_offers(self, obj):
        request = self.context.get('request')
        monthly_offers = obj.filter(type=3)
        monthly_offers = BusinessOffersDetailSerializer(monthly_offers, context={"request": request}, many=True).data[:4]
        return monthly_offers


class OffersHomeListSerializer(serializers.ModelSerializer):
    daily_offers = serializers.SerializerMethodField()
    weekly_offers = serializers.SerializerMethodField()
    monthly_offers = serializers.SerializerMethodField()
    hot_offers = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Offers
        fields = ("daily_offers","weekly_offers","monthly_offers","hot_offers",)

    
    def get_daily_offers(self, obj):
        daily_offers = obj.filter(type=1)[:6]
        daily_offers_list = []
        
        daily_offers = OfferDetailSerializer(daily_offers, many=True).data
        for offer in daily_offers:
            for products in offer['result']:
                if 'offer_type' in products:
                    daily_offers_list.append(products)
                    if len(daily_offers_list) == 6:
                        break
            if len(daily_offers_list) == 6:
                break
        return daily_offers_list

    def get_weekly_offers(self, obj):
        weekly_offers = obj.filter(type=2)[:6]
        weekly_offers = OfferDetailSerializer(weekly_offers, many=True).data
        weekly_offers_list = []

        for offer in weekly_offers:
            for products in offer['result']:
                if 'offer_type' in products:
                    weekly_offers_list.append(products)
                    if len(weekly_offers_list) == 6:
                        break
            if len(weekly_offers_list) == 6:
                break
        return weekly_offers_list
        
    def get_monthly_offers(self, obj):
        monthly_offers = obj.filter(type=3)[:4]
        monthly_offers = OfferDetailSerializer(monthly_offers, many=True).data
        monthly_offers_list = []

        for offer in monthly_offers:
            for products in offer['result']:
                if 'offer_type' in products:
                    monthly_offers_list.append(products)
                    if len(monthly_offers_list) == 6:
                        break
            if len(monthly_offers_list) == 6:
                break
        return monthly_offers_list
    
    def get_hot_offers(self, obj):
        hot_offers = obj.filter(type=4)[:6]
        hot_offers = OfferDetailSerializer(hot_offers, many=True).data
        hot_offers_list = []

        for offer in hot_offers:
            for products in offer['result']:
                if 'offer_type' in products:
                    hot_offers_list.append(products)
                    if len(hot_offers_list) == 6:
                        break
            if len(hot_offers_list) == 6:
                break
        return hot_offers_list
    

class HotOffersListSerializer(serializers.ModelSerializer):
    hot_offers = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Offers
        fields = ("hot_offers",)

    def get_hot_offers(self, obj):
        hot_offers = BusinessOffersDetailSerializer(obj, many=True).data
        return hot_offers
   
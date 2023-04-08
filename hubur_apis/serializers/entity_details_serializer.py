from hubur_apis import models
from rest_framework import serializers
import global_methods
from datetime import datetime
from django.db.models import Q
from django.db.models import Case, When
import calendar
from hubur_apis.serializers.search_serializer import SubCatagoriesListSerializer

class CheckinStoryListSerializer(serializers.ModelSerializer):
    checkin_story = serializers.ImageField(source="i_story.image")
    class Meta:
        model = models.Checkedin
        fields = ('checkin_story',)

class GalleryImagesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Images
        fields = ("id","image",)

class BusinessListSerializer(serializers.ModelSerializer):
    i_category = serializers.CharField(source="i_category.name")
    i_subcategory = SubCatagoriesListSerializer(many=True)
    class Meta:
        model = models.Business
        fields = ("id","name","country_code","contact","address","long","lat","website","logo_pic","i_category","i_subcategory","is_claimed",)
    
    def to_representation(self, data):
        now = datetime.now()
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
        
            
            if user_id != None:
                user_long = request.user.long
                user_lat = request.user.lat
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
        del response['logo_pic'], response['i_subcategory'], response['long'], response['lat']
        response['reviews'] = []
        response['rating'] = ""
        if response['i_category'] == "Products":
            response['products'] = []

        
        day_name = now.strftime('%A')
        time_str = now.strftime('%H:%M:%S')
        current_time = datetime.strptime(time_str, '%H:%M:%S').time()
        
        business_status_obj = models.BusinessSchedule.objects.filter(i_business=data,i_day__name=day_name)

        if not business_status_obj:
            response['status'] = "open"
            response['close_time'] = "24 hours open"
            response['open_time'] =  ""
        else:
            business_status_obj = business_status_obj.first()

            
            if business_status_obj.start_time is None or business_status_obj.end_time is None:
                response['status'] = "open"
                response['close_time'] = "24 hours open"
                response['open_time'] =  ""
            elif business_status_obj.is_active == True:
                start_time = datetime.combine(now.date(), business_status_obj.start_time)
                end_time = datetime.combine(now.date(), business_status_obj.end_time)
            
                if current_time >= start_time.time() and current_time < end_time.time():
                    response['status'] = 'open'
                    response['close_time'] =  end_time.strftime('%I:%M %p')
                    response['open_time'] =  ""
                else:
                    business_schedule_obj = models.BusinessSchedule.objects.filter(i_business=data, is_active=True).exclude(i_day__name=day_name).exclude(Q(start_time__isnull=True) | Q(start_time=None)).order_by(Case(
                            *[When(i_day__name=value, then=index) for index, value in enumerate(weekday_names)],
                            default=len(weekday_names)
                        ))
                    if business_schedule_obj:
                        business_schedule_obj = business_schedule_obj.first()
                        response['status'] = "closed"
                        response['open_time'] =business_schedule_obj.i_day.name +" " +business_schedule_obj.start_time.strftime('%I:%M %p')
                        response['close_time'] = ""
                    else:
                        response['status'] = "closed"
                        response['open_time'] =""
                        response['close_time'] = ""
            else:
                weekday_names = list(calendar.day_name)

                business_schedule_obj = models.BusinessSchedule.objects.filter(i_business=data, is_active=True).exclude(i_day__name=day_name).exclude(Q(start_time__isnull=True) | Q(start_time=None)).order_by(Case(
                            *[When(i_day__name=value, then=index) for index, value in enumerate(weekday_names)],
                            default=len(weekday_names)
                        ))

                if business_schedule_obj:
                    business_schedule_obj = business_schedule_obj.first()
                    response['status'] = "closed"
                    response['open_time'] =business_schedule_obj.i_day.name +" " +business_schedule_obj.start_time.strftime('%I:%M %p')
                    response['close_time'] = ""
                else:
                    response['status'] = "closed"
                    response['open_time'] =""
                    response['close_time'] = ""
                    
            
        checkin_storys_obj = models.Checkedin.objects.filter(i_business_id=data.id, i_story__is_active = True).exclude(i_story__video = None)
        checkin_storys_serializer = CheckinStoryListSerializer(checkin_storys_obj,many=True)
        if checkin_storys_serializer:
            checkin_storys_list = []
            for i in checkin_storys_serializer.data:
                checkin_storys_list.append(i['checkin_story'])
            response['checkin_storys'] = checkin_storys_list
        else:
            response['checkin_storys'] = []

        gallery_images_list = []
        gallery_images = models.Images.objects.filter(i_business=data, is_active=True)
        if gallery_images:
            gallery_images = GalleryImagesListSerializer(gallery_images,many=True)
            for images in gallery_images.data:
                gallery_images_list.append(images['image'])

        response['gallery_images'] = gallery_images_list
        return response
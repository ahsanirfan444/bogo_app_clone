from global_methods import getCurrentLanguageContextForAppUsers, keyvalue
from hubur_apis import models
from rest_framework import serializers
from datetime import datetime,timezone

from hubur_apis.serializers.story_serializer import BusinessLogoSerializer


class CreateBookingSerializer(serializers.ModelSerializer):
    persons = serializers.IntegerField(allow_null=False)
    class Meta:
        model = models.Booking
        fields = ("persons","date","i_business",)
    
    def create(self, validated_data):
        user_obj = self.context.get('user_obj')
        validated_data['i_user'] = user_obj
        return validated_data


    def validate(self, data):
        user_obj = self.context.get('user_obj')
        business = data['i_business']
        booking_date = data['date']
        persons = data['persons']
        business = models.Business.objects.get(id=business.id, is_active=True, i_user__is_active=True)
        business_cat = business.i_category.name
        current_datetime = datetime.now(timezone.utc)
        if persons <= 0:
            raise serializers.ValidationError("You have entered invalid number")
        if booking_date <= current_datetime:
            raise serializers.ValidationError("Please enter a booking date that is today or later.")
        else:
            if not business_cat == 'Restaurant':
                raise serializers.ValidationError("This business is not a Restaurant")
            else:
                if business.is_claimed == 1:
                    raise serializers.ValidationError("This Restaurant is not claimed by anyone")
                else:
                    booking_limit = models.Booking.objects.filter(i_business=business, i_user=user_obj, date__date=booking_date.date()).count()
                    if booking_limit >= 3:
                        raise serializers.ValidationError("You have reached max limit of booking")
                    else:
                        check_booking = models.Booking.objects.filter(i_business=business, i_user=user_obj, date=booking_date)
                        if check_booking:
                            raise serializers.ValidationError("You have already booked this time slot")
                        else:
                            day_name = booking_date.strftime('%A')
                            business_status_obj = models.BusinessSchedule.objects.filter(i_business=business,i_day__name=day_name)

                            if business_status_obj:
                                business_status = business_status_obj.first()
                                if business_status.is_active == False:
                                    raise serializers.ValidationError("The restaurant is closed during the time you entered. Please try a different time.")
                                else:
                                    if business_status.start_time is None or business_status.end_time is None:
                                        return data
                                    else:
                                        is_open = models.BusinessSchedule.objects.filter(i_business=business,i_day__name=day_name, start_time__lte=booking_date.time(), end_time__gte=booking_date.time(), is_active=True).exists()
                                        if not is_open:
                                            raise serializers.ValidationError("The restaurant is closed during the time you entered. Please try a different time.")
                                        else:
                                            return data
                            else:
                                return data

class GetAllBookingSerializer(serializers.ModelSerializer):
    business_id = serializers.IntegerField(source = "i_business.id")
    business_name = serializers.CharField(source = "i_business.name")
    business_cat = serializers.CharField(source = "i_business.i_category.name")
    i_business = serializers.SerializerMethodField() 
    status = serializers.SerializerMethodField("get_status")
    class Meta:
        model = models.Booking
        fields = ("persons","date","booking_no","i_business","status","reason","business_id","business_name","business_cat",)

    def get_i_business(self, obj):
        logo_pic = BusinessLogoSerializer(obj.i_business).data['logo_pic']
        return logo_pic
    
    def to_representation(self, instance):
        response =  super().to_representation(instance)
        response['business_logo'] = response['i_business']
        del response['i_business']
        return response

    def get_status(self,obj):
        request = self.context.get('request')
        lang_obj = getCurrentLanguageContextForAppUsers(request)
        name = keyvalue(lang_obj, obj.get_status_display())
        return name
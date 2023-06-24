
from hubur_apis import models
from rest_framework import serializers
import notifications
from datetime import datetime
from django.db.models import Q
from django.db.models import Case, When
import calendar

class ClaimBusinessSerializer(serializers.ModelSerializer):
    trade_license = serializers.FileField(max_length=None, allow_null=True)
    class Meta:
        model = models.ClaimBusiness
        fields = ['first_name','last_name','business_email','trade_license_number','i_business','trade_license']

    def create(self, validated_data):
        data = models.ClaimBusiness.objects.create(**validated_data) 
        body = "We are reviewing. Your request has been sent for claiming."
        to = validated_data['business_email']
        subject = "Claim Business"
        notifications.sendEmailToSingleUser(body, to, subject)
        return super(ClaimBusinessSerializer, self).validate(data)
    
    def validate_trade_license(self,value):
        if value:
            all_ext_list = ['rgb', 'gif',' pbm',' pgm',' ppm',' tiff', 'rast', 'xbm', 'jpeg','jpg', 'bmp', 'png', 'webp', 'exr','pdf','docx',
                            'docm','dotx','dotm','docb','wll','wwl','xls','xlt','xlm','xll_','xla_','pptx','potx','xlsx']
            file_name = value.name
            file_name = file_name.replace(" ","_").replace("-","_")
            file_extension = (file_name.split('.')[1]).lower()
            if file_extension in all_ext_list:
                return value
            else:
                raise serializers.ValidationError("Not a valid file")   
        else:
            raise serializers.ValidationError("No File is uploaded")

    def validate_i_business(self,value):
        if value:
            business_obj = models.Business.objects.filter(id=value.id, is_active=True).exists()
            if business_obj:
                return value
            else:
                raise serializers.ValidationError("No Business Found")

    def validate_business_email(self,value):
        business_obj = models.Business.objects.filter(i_user__email=value, is_active=True).exists()
        claim_business_obj = models.ClaimBusiness.objects.filter(business_email=value).exists()
        if business_obj:
            raise serializers.ValidationError("Business is already exist with this email")
        elif claim_business_obj:
            raise serializers.ValidationError("This email already exist. Try different one")
        else:
            return value
            
    def validate_trade_license_number(self,value):
        claim_business_obj = models.ClaimBusiness.objects.filter(trade_license_number=value).exists()
        if claim_business_obj:
            raise serializers.ValidationError("Entered trade license number already exist. Try different one")
        else:
            return value

class BusinessListSerializer(serializers.ModelSerializer):
    class Meta:
         model = models.Business
         fields = ("id","name","place_id",)



class BusinessSerializerForTimeOnly(serializers.ModelSerializer):
    
    class Meta:
        model = models.Business
        fields = ("id",)

    def to_representation(self, data):
        now = datetime.now()

        weekday_names = list(calendar.day_name)
        response = super().to_representation(data)


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
        return response
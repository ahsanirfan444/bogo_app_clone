from datetime import datetime
import json
import os
import random
from django.core.exceptions import ValidationError
from rest_framework import serializers
import math
from hubur.settings.base import BASE_DIR
from hubur_apis import models
from push_notifications.models import WebPushDevice, GCMDevice

def generate_otp_tokens():
    code_dict = dict()
    code_dict['email_code'] = ''.join(str(random.randint(1, 9)) for _ in range(0, 4))
    code_dict['sms_code'] = ''.join(str(random.randint(1, 9)) for _ in range(0, 4))
    return code_dict

HD404 = "User is not verifed"

def file_size(value):
    limit = int(os.getenv("FILE_UPLOAD_LIMIT"))
    limit_text = os.getenv("FILE_UPLOAD_LIMIT_TEXT")
    if value.size > limit:
        raise ValidationError(f'Min upload size is {limit_text}.')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid
        
        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')
    
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)
    
    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension



def distance(lat1, lon1, lat2, lon2):
    try:
        R = 6371  # Radius of the earth in km

        # Convert latitude and longitude to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        distance = str(round(distance, 2))
        #return distance in KM
        return distance
    except:
        return 0

def get_categories_list():
    try:
        return list(models.Category.objects.filter(is_active=True).values_list('name', flat=True))
    except:
        pass

def get_booking_number():
    return datetime.now().strftime('%d%H%M%S')

def format_number(value):
    if value >= 1000000000:
        return '{:.1f}B'.format(value/1000000000)
    elif value >= 1000000:
        return '{:.1f}M'.format(value/1000000)
    elif value >= 1000:
        return '{:.1f}k'.format(value/1000)
    else:
        return str(value)
    

def create_content_images(images, user, type, business, content):
    try:
        for image in images:
            models.Images.objects.create(
                image=image, i_user=user, type=type, i_business=business, i_content=content
            )
        return True
    
    except Exception:
        return
    

def delete_content_images(image_ids, user, type, business):
    try:
        for id in image_ids:
            models.Images.objects.filter(
                id=id, i_user=user, type=type, i_business=business
            ).delete()

        return True
    
    except Exception:
        return
    
def pause_notifications_for_update_on_whatsapp(user_id):

    update_on_whatsapp = models.NotificationSettings.objects.filter(i_user_id__in=user_id, update_on_whatsapp=False)
    if update_on_whatsapp.exists():
        user_ids = list(update_on_whatsapp.values_list('i_user_id', flat=True))
        return user_ids
    return []

def pause_notifications_promotional_messages(userID):

    promotional_messages = models.NotificationSettings.objects.filter(i_user_id__in=userID,promotional_messages=False)
    if promotional_messages.exists():
        user_ids = list(promotional_messages.values_list('i_user_id', flat=True))
        return user_ids
    return []
    
def pause_notifications_promotional_email(user_id):

    promotional_email = models.NotificationSettings.objects.filter(i_user_id__in=user_id,promotional_email=False)
    if promotional_email.exists():
        user_ids = list(promotional_email.values_list('i_user_id', flat=True))
        return user_ids
    return []
    
def pause_all_notifications(user_id):

    all_notifications = models.NotificationSettings.objects.filter(i_user_id__in=user_id,all_notifications=False)
    if all_notifications.exists():
        user_ids = list(all_notifications.values_list('i_user_id', flat=True))
        return user_ids
    return []
    
def pause_notifications_new_offer(user_id, notification_type):

    new_offer = models.NotificationSettings.objects.filter(i_user_id__in=user_id,new_offer=False)
    if new_offer.exists() and notification_type == 6:
        user_ids = list(new_offer.values_list('i_user_id', flat=True))
        return user_ids
    return []
    
def pause_notifications_offer_expire(user_id, notification_type):

    offer_exipire = models.NotificationSettings.objects.filter(i_user_id__in=user_id,offer_expire=False)
    if offer_exipire.exists() and notification_type == 5:
        user_ids = list(offer_exipire.values_list('i_user_id', flat=True))
        return user_ids
    return []
    
def manage_online_status(user, status):
    query = models.UserOnlineStatus.objects
    query.filter(i_user=user).delete()
    query.update_or_create(i_user=user, is_online=status)
    return query

def AddRewardPoints(type, user, business, content):
    try:
        reward_points = models.RewardPoints.objects.get(type=type)
        instance = models.UserReward.objects.create(i_user=user, i_business=business, i_content=content, i_point=reward_points)
        return instance
    except Exception:
        return


def localized_subcategory_name(request, sub_category):
    try:
        if request.user.is_authenticated:
            if request.user.lang_code == 1:
                return sub_category.i_subcatagory.name
            else:
                return sub_category.i_subcatagory.name_ar

        else:
            if request.headers.get('Accept-Language') == str(1):
                return sub_category.i_subcatagory.name
            else:
                return sub_category.i_subcatagory.name_ar

    except Exception as e:
        # print(e)
        pass

def keyvalue(dict, key):    
    return dict[key]


def getCurrentLanguageContextForAppUsers(request):
    output = None
    try:
        if request.user.lang_code == 1:
            with open(os.path.join(BASE_DIR, 'locale/en.json'), encoding="utf-8") as file:
                output = json.load(file)
        else:
            with open(os.path.join(BASE_DIR, 'locale/ar.json'), encoding="utf-8-sig") as file:
                output = json.load(file)

    except Exception as e:
        # print(e)
        if request.headers.get('Accept-Language') == str(1):
            with open(os.path.join(BASE_DIR, 'locale/en.json'), encoding="utf-8") as file:
                output = json.load(file)
        else:
            with open(os.path.join(BASE_DIR, 'locale/ar.json'), encoding="utf-8-sig") as file:
                output = json.load(file)
    
    return output


def create_tags(tags, content):
    if tags:
        for tag in tags:
            if not tag.isdigit():
                try:
                    new_tag = models.Tags(name=tag, content=content)
                    new_tag.save()
                except Exception as e:
                    print(e)
                    raise ValidationError(str(e))
            
    return tags
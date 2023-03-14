import os
import random
from django.core.exceptions import ValidationError
from rest_framework import serializers
import math

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
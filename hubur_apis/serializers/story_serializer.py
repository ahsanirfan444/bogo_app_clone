
from hubur_apis import models
from rest_framework import serializers
from datetime import datetime, timedelta, timezone
from django.utils.timesince import timesince

class ImageSerializer(serializers.ModelSerializer):
    file = serializers.FileField(max_length=None, allow_null=True)
    class Meta:
        model = models.Story
        fields = ['i_business','file','caption']
    
    def create(self, validated_data):
        user_obj = self.context.get('user_obj')
        validated_data['i_user'] = validated_data['updated_user'] = user_obj
        file_obj = validated_data['file']['story']

        if validated_data['file']['status'] == 'image':
            validated_data['image'] = file_obj
            del validated_data['file']
            validated_data['i_story'] = models.Story.objects.create(**validated_data)
            validated_data['file'] = file_obj
            return validated_data
        elif validated_data['file']['status'] == 'video':
            validated_data['video'] = file_obj
            del validated_data['file']
            validated_data['i_story'] = models.Story.objects.create(**validated_data)
            validated_data['file'] = file_obj
            return validated_data
        else:
            raise serializers.ValidationError("Invalid Image")

    def validate_file(self,value):
        if value:
            img_ext_list = ['rgb', 'gif',' pbm',' pgm',' ppm',' tiff', 'rast', 'xbm', 'jpeg','jpg', 'bmp', 'png', 'webp', 'exr']
            video_ext_list = ['webm', 'mpg', 'mp2', 'mpeg', 'mpe', 'mpv', 'ogg', 'mp4', 'm4p', 'm4v', 'avi', 'wmv', 'mov', 'qt','flv', 'swf', 'avchd']
            file_name = value.name
            file_name = file_name.replace(" ","_").replace("-","_")
            file_extension = (file_name.split('.')[1]).lower()

            data_dict = dict()
            data_dict['story'] = value
            if file_extension in img_ext_list:
                data_dict['status'] = 'image'
                return data_dict
            elif file_extension in video_ext_list:
                data_dict['status'] = 'video'
                return data_dict
            else:
                raise serializers.ValidationError("Not a valid file")
        else:
            raise serializers.ValidationError("No File is uploaded")


    def validate_i_business(self,value):
        business_obj = models.Business.objects.filter(id=value.id, is_active=True).exists()
        if business_obj:
            return value
        else:
            raise serializers.ValidationError("No Business Found")


    def validate(self, data):
            user_obj = self.context.get('user_obj')
            checkin_exist = models.Story.objects.filter(i_user=user_obj,i_business=data['i_business'])
            if checkin_exist:
                checkin_exist = checkin_exist.order_by('-created_at').first()
                cr_time = checkin_exist.created_at
                t2 = cr_time + timedelta(hours=24)
                now = datetime.now(timezone.utc)
                if now < t2:
                    raise serializers.ValidationError("Story already uploaded for this business")
                else:
                    return super().validate(data)
                
            else:
                return super().validate(data)
            
class UserPicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('profile_picture',)

class BusinessLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Business
        fields = ('logo_pic',)


class StoriesSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source = "i_user.first_name")
    last_name = serializers.CharField(source = "i_user.last_name")
    user_id = serializers.IntegerField(source = "i_user.id")
    i_business = serializers.SerializerMethodField()
    i_user = serializers.SerializerMethodField()
    class Meta:
        model = models.Story
        fields = ("id","caption","video","image","updated_at","user_id","first_name","last_name","i_business","i_user",)

    def get_i_business(self, obj):
        logo_pic = BusinessLogoSerializer(obj.i_business).data['logo_pic']
        return logo_pic
    
    def get_i_user(self, obj):
        profile_pic = UserPicSerializer(obj.i_user).data['profile_picture']
        return profile_pic

    def to_representation(self, instance):
        response = super().to_representation(instance)
        

        now = datetime.now(timezone.utc) 
        story_creation_time = datetime.strptime(response['updated_at'], "%Y-%m-%dT%H:%M:%S.%f%z")

        time_difference = timesince(story_creation_time, now)
        response['created_at'] = time_difference + " ago"
        response['logo_pic'] = response['i_business']
        response['user_profile_pic'] = response['i_user']
        del response['updated_at'],response['i_business'], response['i_user']
        
        response['user'] = response['first_name'] + " " + response['last_name']        
        del response['first_name'],response['last_name']

        return response
        


class StoryListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="i_category")

    class Meta:
        model = models.Business
        fields = ("id","name","address","long","lat","category",)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('context')
        super().__init__(*args, **kwargs)

    def get_full_url(self):
        request = self.context.get('request')
        url = models.Business.logo_pic.url
        return request.build_absolute_uri(url)
    
    def to_representation(self, data):
        response = super().to_representation(data)
        story_obj = models.Story.objects.filter(i_business=data).order_by("-created_at")[:2]
        serializer = StoriesSerializer(story_obj, many=True)
        response['story'] =  serializer.data
        

        return response
    

class BusinessStoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Business
        fields = ("id","name","address",)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('context')
        super().__init__(*args, **kwargs)

    def get_full_url(self):
        request = self.context.get('request')
        url = models.Business.logo_pic.url
        return request.build_absolute_uri(url)
    
    def to_representation(self, data):
        response = super().to_representation(data)
        return response
    
class UserStoriesSerializer(serializers.ModelSerializer):
    business_id = serializers.IntegerField(source = "i_business.id")
    business_name = serializers.CharField(source = "i_business.name")
    business_category = serializers.CharField(source = "i_business.i_category.name")
    i_business = serializers.SerializerMethodField()

    class Meta:
        model = models.Story
        fields = ("id","caption","video","image","updated_at","business_id","business_name","business_category","i_business","is_active",)

    def get_i_business(self, obj):
        logo_pic = BusinessLogoSerializer(obj.i_business).data['logo_pic']
        return logo_pic

    def to_representation(self, instance):
        response = super().to_representation(instance)
        

        now = datetime.now(timezone.utc) 
        story_creation_time = datetime.strptime(response['updated_at'], "%Y-%m-%dT%H:%M:%S.%f%z")

        time_difference = timesince(story_creation_time, now)
        response['created_at'] = time_difference + " ago"
        response['business_logo'] = response['i_business']
        del response['updated_at'], response['i_business']

        return response

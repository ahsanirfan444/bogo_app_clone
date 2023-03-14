
from hubur_apis import models
from rest_framework import serializers


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
            models.Story.objects.create(**validated_data)
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

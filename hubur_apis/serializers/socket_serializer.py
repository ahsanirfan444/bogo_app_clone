from global_methods import distance, format_number
from hubur_apis import models
from rest_framework import serializers
from hubur_apis.serializers.review_serializer import AggregateBusinessReviewsSerializer
from hubur_apis.serializers.search_serializer import SubCatagoriesListSerializer

from hubur_apis.serializers.story_serializer import StoriesSerializer




class SocketSerializer(serializers.ModelSerializer):
    i_subcategory = serializers.IntegerField(required=False, allow_null=True)
    class Meta:
         model = models.Business
         fields = ("long","lat","i_subcategory","is_featured",)


class MapBusinessSerializer(serializers.ModelSerializer):
    i_category = serializers.CharField(source="i_category.name")
    i_subcategory = serializers.SerializerMethodField()
    class Meta:
        model = models.Business
        fields = ("id","name","logo_pic","long","lat","i_category","i_subcategory","is_featured",)
    
    def get_i_subcategory(self,obj):
        obj_data = list(obj.i_subcategory.all().values_list('name',flat=True))
        return obj_data



    
    def to_representation(self, data):
        response = super().to_representation(data)
        story_obj = models.Story.objects.filter(i_business=data, is_active=True).order_by("-created_at")[:2]
        serializer = StoriesSerializer(story_obj, many=True)
        story_list = []
        for story in serializer.data:
            if story['image'] is not None:
                story_list.append(story['image'])
            else:
                story_list.append(story['video'])
            if len(story_list) == 1:
                break
        
        response['story'] =  story_list

        user_long = self.context.get('user_long')
        user_lat = self.context.get('user_lat')

        if user_lat == user_long == 0:
            response['total_distance'] = 0.0
        else:    
            total_distance = distance(user_lat,user_long,data.lat,data.long)
            response['total_distance'] = float(total_distance)
        return response


class SearchBusinessInMapSerializer(serializers.ModelSerializer):
    i_category = serializers.CharField(source='i_category.name')
    attributes = serializers.SerializerMethodField("get_i_attributes")
    i_sub_category = serializers.SerializerMethodField()
    class Meta:
         model = models.Business
         fields = ("id","name","attributes","address","i_sub_category","logo_pic","i_category","long","lat","is_featured",)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('context')
        super().__init__(*args, **kwargs)

    def get_full_url(self):
        request = self.context.get('request')
        url = models.Business.logo_pic.url
        return request.build_absolute_uri(url)
    
    def get_i_attributes(self,obj):
        if obj.i_category == 'Restaurant':
            attributes = obj.i_attributes.all().values_list('name',flat=True)
            return attributes
        else:
            return []
    
    def get_i_sub_category(self,obj):
        obj_data = list(obj.i_subcategory.all().values_list('name',flat=True))
        return obj_data
    
    def to_representation(self, data):
        response = super().to_representation(data)


        user_long = self.context.get('user_long')
        user_lat = self.context.get('user_lat')

        total_checkins = models.Checkedin.objects.filter(i_business=data).exclude(i_user__is_active=False).count()
        total_checkins = format_number(total_checkins)
        response['checkins'] = total_checkins
    
        if user_lat == user_long == 0:
            response['total_distance'] = 0.0
        else:    
            total_distance = distance(user_long,user_lat,data.long,data.lat)
            response['total_distance'] = float(total_distance)

        reviews = AggregateBusinessReviewsSerializer(data).data
        response['total_reviews'] = reviews['total_reviews']
        response['average_rate'] = reviews['average_rate']

        return response
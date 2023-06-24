
from hubur_apis import models
from rest_framework import serializers
from hubur_apis.serializers.content_serializer import ProductImagesListSerializer
from hubur_apis.serializers.story_serializer import BusinessLogoSerializer

class RewardSerializer(serializers.ModelSerializer):
    type_id = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()
    point_type = serializers.SerializerMethodField("get_point_type")
    
    class Meta:
        model = models.UserReward
        fields = ("id","type_id","name","type","address","description","logo","points","point_type",)

    def get_type_id(self, obj):
        if obj.i_content:
            return obj.i_content.id
        else:
            return obj.i_business.id

    def get_points(self,data):
        return data.i_point.points
    
    def get_business_logo(self, obj):
        logo_pic = BusinessLogoSerializer(obj.i_business).data['logo_pic']
        return logo_pic
    
    def get_logo(self, obj):
        if obj.i_content:
            logo_pic = models.Images.objects.filter(is_active=True,i_content=obj.i_content).order_by('-created_at').first()
            logo_pic = (ProductImagesListSerializer(logo_pic)).data['image']
        else:
            logo_pic = BusinessLogoSerializer(obj.i_business).data['logo_pic']
        return logo_pic
        
    def get_name(self, obj):
        if obj.i_content:
            return obj.i_content.name
        else:
            return obj.i_business.name
        
    def get_type(self, obj):
        if obj.i_content:
            return "Content"
        else:
            return "Business"
        
    def get_address(self, obj):
        if obj.i_content:
            return ""
        else:
            return obj.i_business.address
        
    def get_description(self, obj):
        if obj.i_content:
            return obj.i_content.description
        else:
            return ""
        
    def get_point_type(self,data):
        return data.i_point.get_type_display()
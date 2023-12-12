
from hubur_apis import models
from rest_framework import serializers
from django.db.models import Avg
from global_methods import format_number
from hubur_apis.serializers.user_serializer import GetUserProfileSerializer
from datetime import datetime

class ProductImagesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Images
        fields = ("image",)

class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reviews
        fields = ("review","i_content","rate",)
    
    def create(self, validated_data):
        user_obj = self.context.get('user_obj')
        validated_data['i_user'] = user_obj
        i_business = validated_data['i_content'].i_business
        validated_data['i_business'] = i_business
        return validated_data
        
    def validate(self, data):
        user_obj = self.context.get('user_obj')
        i_content = data['i_content']
        i_business = i_content.i_business
        
        reviewed_content = models.Reviews.objects.filter(i_user=user_obj,i_content=i_content, i_business = i_business, created_at__date=datetime.now().date()).exists()
        if reviewed_content:
            raise serializers.ValidationError("You have already reviewed")
        else:
            if i_business.is_active and i_content.is_active:
                return data
            else:
                raise serializers.ValidationError("This business is inactive")


class GetAllReviewsSerializer(serializers.ModelSerializer):
    content_id = serializers.IntegerField(source="i_content.id", default=None)
    content_name = serializers.CharField(source="i_content.name",default=None)
    user_id = serializers.IntegerField(source="i_user.id", default=None)
    user_name = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()
    content_image = serializers.SerializerMethodField()
    user_status = serializers.SerializerMethodField('get_user_status')

    class Meta:
        model = models.Reviews
        fields = ("id","review","rate","user_id","user_name","content_id","content_name","profile_pic","content_image","created_at","display_name","display_image", "user_status",)

    def get_user_name(self,obj):
        if obj.i_user:
            return obj.i_user.get_name()
        else:
            return ""
    
    def get_profile_pic(self,obj):
        if obj.i_user:
            profile_pic = obj.i_user.profile_picture.url
            return profile_pic
        else:
            return ""
    
    def get_content_image(self,obj):
        if obj.i_content:
            images = models.Images.objects.filter(is_active=True,i_content=obj.i_content).order_by('-created_at').first()
            content_image = (ProductImagesListSerializer(images)).data['image']
            return content_image
        else:
            return ""
        

    def get_user_status(self,obj):
        try:
            return obj.i_user.is_active
        except Exception:
            return False


class AggregateReviewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Content
        fields = ("id",)

    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        content_id = response['id']
        del response['id']
        five_star = models.Reviews.objects.filter(i_content=content_id, rate__gte=4.5, rate__lte=5.0).count()
        four_star = models.Reviews.objects.filter(i_content=content_id, rate__gte=3.5, rate__lte=4.4).count()
        three_star = models.Reviews.objects.filter(i_content=content_id, rate__gte=2.5, rate__lte=3.4).count()
        two_star = models.Reviews.objects.filter(i_content=content_id,rate__gte=1.5, rate__lte=2.4).count()
        one_star = models.Reviews.objects.filter(i_content=content_id, rate__gte=0.0, rate__lte=1.4).count()
        all_reviews = models.Reviews.objects.filter(i_content=content_id)
        if len(all_reviews) != 0:
            total_reviews = all_reviews.count()
        else:
            total_reviews = 1


        
        response['five_star'] = float("{:.1f}".format(five_star/total_reviews))
        response['five_star_converted'] = format_number(five_star)
        
        response['four_star'] = float("{:.1f}".format(four_star/total_reviews))
        response['four_star_converted'] = format_number(four_star)
        
        response['three_star'] = float("{:.1f}".format(three_star/total_reviews))
        response['three_star_converted'] = format_number(three_star)
        
        response['two_star'] = float("{:.1f}".format(two_star/total_reviews))
        response['two_star_converted'] = format_number(two_star)

        response['one_star'] = float("{:.1f}".format(one_star/total_reviews))
        response['one_star_converted'] = format_number(one_star)

        
        response['total_reviews'] = format_number(all_reviews.count())
        average_rate =  all_reviews.aggregate(avg_rate=Avg('rate'))['avg_rate']
        if average_rate:
            response['average_rate'] = float("{:.2f}".format(average_rate))
        else:
            response['average_rate'] = 0.0
        return response
    

class AggregateBusinessReviewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Business
        fields = ("id", "is_featured",)

    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        business_id = response['id']
        del response['id']

        five_star = models.Reviews.objects.filter(i_business=business_id, rate__gte=4.5, rate__lte=5.0).count()
        four_star = models.Reviews.objects.filter(i_business=business_id, rate__gte=3.5, rate__lte=4.4).count()
        three_star = models.Reviews.objects.filter(i_business=business_id, rate__gte=2.5, rate__lte=3.4).count()
        two_star = models.Reviews.objects.filter(i_business=business_id,rate__gte=1.5, rate__lte=2.4).count()
        one_star = models.Reviews.objects.filter(i_business=business_id, rate__gte=0.0, rate__lte=1.4).count()
        all_reviews = models.Reviews.objects.filter(i_business=business_id)
        
        if len(all_reviews) != 0:
            total_reviews = all_reviews.count()
        else:
            total_reviews = 1
        
        response['five_star'] = float("{:.1f}".format(five_star/total_reviews))
        response['five_star_converted'] = format_number(five_star)
        
        response['four_star'] = float("{:.1f}".format(four_star/total_reviews))
        response['four_star_converted'] = format_number(four_star)
        
        response['three_star'] = float("{:.1f}".format(three_star/total_reviews))
        response['three_star_converted'] = format_number(three_star)
        
        response['two_star'] = float("{:.1f}".format(two_star/total_reviews))
        response['two_star_converted'] = format_number(two_star)

        response['one_star'] = float("{:.1f}".format(one_star/total_reviews))
        response['one_star_converted'] = format_number(one_star)



        
        response['total_reviews'] = format_number(all_reviews.count())
        average_rate =  all_reviews.aggregate(avg_rate=Avg('rate'))['avg_rate']
        if average_rate:
            response['average_rate'] = float(round(average_rate,1))
        else:
            response['average_rate'] = 0.0
        return response

from hubur_apis import models
from rest_framework import serializers
from hubur_apis.serializers.entity_details_serializer import GalleryImagesListSerializer

from hubur_apis.serializers.story_serializer import BusinessLogoSerializer
from hubur_apis.serializers.voting_serializer import GetAllVotingSerializer

class CampaignListSerializer(serializers.ModelSerializer):

    
    business_id = serializers.CharField(source="i_business.id", default=None)
    business_name = serializers.CharField(source="i_business.name", default=None)
    business_address = serializers.CharField(source="i_business.address", default=None)
    business_logo = serializers.SerializerMethodField()
    business_image = serializers.SerializerMethodField()
    vote = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('context')
        super().__init__(*args, **kwargs)
        
        try:
            request = self.context.get('request')
            if request.user.is_authenticated:
                if request.user.lang_code == 1:
                    del self.fields['title_ar']
                    del self.fields['desc_ar']
                else:
                    self.fields['title'] = self.fields['title_ar']
                    self.fields['desc'] = self.fields['desc_ar']

            else:
                del self.fields['vote']
                if request.headers.get('Accept-Language') == str(1):
                    del self.fields['title_ar']
                    del self.fields['desc_ar']
                else:
                    self.fields['title'] = self.fields['title_ar']
                    self.fields['desc'] = self.fields['desc_ar']

        except Exception as e:
            # print(e)
            pass

    class Meta:
        model = models.Campaign
        fields = ("id","title","title_ar","desc","desc_ar","business_id","business_logo","business_address","business_name","business_image","vote",)

    def get_business_logo(self, obj):
        logo_pic = BusinessLogoSerializer(obj.i_business).data['logo_pic']
        return logo_pic
    
    def get_business_image(self, obj):
        gallery_image_query = models.Images.objects.filter(i_business=obj.i_business, type=1)
        if gallery_image_query:
            gallery_image = GalleryImagesListSerializer(gallery_image_query.first()).data['image']
        else:
            gallery_image = ""
        return gallery_image
    
    def get_vote(self, obj):
        request = self.context.get('request')
        response = ""
        if request.user.is_authenticated:
            vote_query = models.Voting.objects.filter(i_business=obj.i_business, i_user=request.user)
            if vote_query:
                response = GetAllVotingSerializer(vote_query.first())
                return response.data['vote'] 
        return response
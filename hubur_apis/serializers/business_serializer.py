
from hubur_apis import models
from rest_framework import serializers
import notifications
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

from hubur_apis import models
from rest_framework import serializers
import string
import random
import datetime
from datetime import timezone
from django.db.models import Q


class RedemptionCodeSerializer(serializers.ModelSerializer):
    code = serializers.CharField(read_only=True)
    i_user = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Redemption
        fields = ['i_content', 'code','i_user']

    def create(self, validated_data):
        user_obj = self.context.get('user_obj')
        validated_data['i_user'] = user_obj.id
        return validated_data

    def validate(self, data):
        user_obj = self.context.get('user_obj')
        content = data['i_content']
        code_length = 11
        code = str(''.join(random.choices(string.ascii_uppercase + string.digits, k=code_length)))
        exist_code = models.Redemption.objects.filter(code=code).exists()
        if exist_code:
            code = str(''.join(random.choices(string.ascii_uppercase + string.digits, k=code_length)))
        query = Q(i_content=content, i_user=user_obj, created_at__date=datetime.datetime.now().date())
        user_redemption = models.Redemption.objects.filter(query).exists()
        if user_redemption:
            raise serializers.ValidationError("You have already redempted this content")

        data['code'] = code

        offer = models.Offers.objects.filter(i_content=content, is_active=True, is_expiry=False).exists()
        if offer:
            return super().validate(data)
        else:
            raise serializers.ValidationError("Offer is not valid for this content")



class RedemptionSerializer(serializers.ModelSerializer):
    i_user = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Redemption
        fields = ['i_content', 'code','i_user']

    def create(self, validated_data):
        user_obj = self.context.get('user_obj')
        validated_data['i_user'] = user_obj.id
        return validated_data

    def validate(self, attrs):
        content = attrs['i_content']
        code = attrs['code']
        user_obj = self.context.get('user_obj')
        query1 = Q(i_content=content, code=code, i_user=user_obj)
        query2 = Q(i_content=content, i_user=user_obj, created_at__date=datetime.datetime.now().date())
        query3 = Q(code = code)
        existance = models.Redemption.objects.filter(query1 | query2 | query3).exists()
        if existance:
            raise serializers.ValidationError("You have already avail this offer")
        
        if len(code) != 11:
            raise serializers.ValidationError("Code must be 11 characters long and contain only letters and numbers.")
        

        # query = Q(i_content=content, i_user=user_obj)
        # query_main = (Q(query, is_expired=False) | Q(query, is_redeemed=False, is_expired=False))
        # redeem_obj = models.Redemption.objects.filter(query_main)
        # if redeem_obj:
        #     redeem_obj = redeem_obj.order_by('-created_at').first()
        #     redeem_obj.is_expired = True
        #     redeem_obj.expired_at=datetime.datetime.now()
        #     redeem_obj.save()


        offer = models.Offers.objects.filter(i_content=content).exists()
        if offer:
            return super().validate(attrs)
        else:
            raise serializers.ValidationError("Offer is not valid for this content")
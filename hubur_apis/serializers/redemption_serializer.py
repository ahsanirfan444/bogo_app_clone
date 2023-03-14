
from hubur_apis import models
from rest_framework import serializers
import string
import random
import datetime
from django.db.models import Q


class RedemptionSerializer(serializers.ModelSerializer):
    code = serializers.CharField(read_only=True)

    class Meta:
        model = models.Redemption
        fields = ['i_sub_categories', 'i_business', 'code']

    def create(self, validated_data):
        user_obj = self.context.get('user_obj')
        validated_data['i_user'] = user_obj
        code_length = 10
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=code_length))
        validated_data['code'] = str(code)
        models.Redemption.objects.create(**validated_data)
        return validated_data

    def validate(self, attrs):
        sub_categories = attrs['i_sub_categories']
        business = attrs['i_business']
        user_obj = self.context.get('user_obj')
        query = Q(i_sub_categories=sub_categories, i_business=business, i_user=user_obj)
        query_main = (Q(query, is_expired=False) | Q(query, is_redeemed=False, is_expired=False))
        redeem_obj = models.Redemption.objects.filter(query_main)
        if redeem_obj:
            redeem_obj = redeem_obj.order_by('-created_at').first()
            redeem_obj.is_expired = True
            redeem_obj.expired_at=datetime.datetime.now()
            redeem_obj.save()
        
        return super().validate(attrs)

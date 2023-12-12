from django.core.management.base import BaseCommand
from hubur_apis import models
from datetime import datetime, timedelta
from hubur_apis.serializers.chat_serializer import UserInfoForChatSerializer
from hubur_apis.serializers.content_serializer import ContentDetailSerializer
import notifications
import json

class Command(BaseCommand):
    help = "This command will remainder user that your saved offer will expire in 3 hours"

    def handle(self, *args, **options):
        current_time = datetime.now()
        next_day = current_time + timedelta(days=1)

        offers_list = list(models.Offers.objects.filter(is_active=True, is_expiry=False, end__date=next_day.date()).values_list('i_content', flat=True))
        saved_offers = models.SavedOffers.objects.filter(i_content__in=offers_list)
        
        for offer in saved_offers:
            offer_name = offer.i_content.name or ""
            offer_name_ar = offer.i_content.name_ar or ""
            sender_pic = UserInfoForChatSerializer(offer.i_user).data['profile_picture']
            # content_obj = ContentDetailSerializer(offer.i_content).data
            # content_obj = json.dumps(content_obj)

            title = "🚨 Offer expiry soon 🚨"
            msg = "Your saved offer "+offer_name+" will expire with in 3 hours.Please avail this offer to get the discounts on products."
            title_ar = "🚨 ينتهي العرض قريبًا 🚨"
            msg_ar = "عرضك المحفوظ "+ offer_name_ar +" ستنتهي خلال 3 ساعات ، برجاء الاستفادة من هذا العرض للحصول على خصومات على المنتجات."
            
            notifications.sendNotificationToSingleUser(offer.i_user.id, msg, msg_ar, title, title_ar, sender_id=2, content_id=offer.i_content.id, action='offer_expire',notification_type=5, activityAndroid="FLUTTER_NOTIFICATION_CLICK", activityIOS="FLUTTER_NOTIFICATION_CLICK",code=None ,
                                                    sender_user_id=str(offer.i_user.id) ,sender_name=offer.i_user.get_name(), image=sender_pic, content=str(offer.i_content.id), actions='offer_expire')

        self.stdout.write("Executed at %s" % current_time.time())
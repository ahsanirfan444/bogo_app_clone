from django.core.management.base import BaseCommand
from hubur_apis import models
from datetime import datetime, timedelta
import notifications

class Command(BaseCommand):
    help = "This command will remainder user that your saved offer will expire in 3 hours"

    def handle(self, *args, **options):
        current_time = datetime.now()
        next_day = current_time + timedelta(days=1)

        offers_list = list(models.Offers.objects.filter(is_active=True, is_expiry=False, end__date=next_day.date()).values_list('i_content', flat=True))
        saved_offers = models.SavedOffers.objects.filter(i_content__in=offers_list)
        
        for offer in saved_offers:
            content_name = offer.i_content.name
            title = "🚨 Offer expiry soon 🚨"
            msg = "Your saved offer "+content_name+" will expire with in 3 hours.\nPlease avail this offer to get the discounts on products."
            notifications.sendNotificationToSingleUser(offer.i_user.id, msg=msg, title=title, sender_id=2, content_id=offer.i_content.id, action='offer_expire',notification_type=5, activityAndroid="FLUTTER_NOTIFICATION_CLICK", activityIOS="FLUTTER_NOTIFICATION_CLICK")

        self.stdout.write("Executed at %s" % current_time.time())
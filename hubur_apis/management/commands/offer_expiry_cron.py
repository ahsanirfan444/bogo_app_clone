from django.core.management.base import BaseCommand
from hubur_apis import models
from datetime import datetime,timezone


class Command(BaseCommand):
    help = "This command will change the status of offer"

    def handle(self, *args, **options):
        current_time = datetime.now()
        models.Offers.objects.filter(is_active=True, is_expiry=False, end__lte=current_time).update(is_active=False, is_expiry=True)
        
        self.stdout.write("Executed at %s" % current_time.time())
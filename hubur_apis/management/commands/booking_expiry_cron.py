from django.core.management.base import BaseCommand
from hubur_apis import models
from datetime import datetime

class Command(BaseCommand):
    help = "This command will change the status of Bookings"

    def handle(self, *args, **kwargs):
        now = datetime.now()
        models.Booking.objects.filter(date__lte=now, status=1).update(status=4)
        
        self.stdout.write("Executed at %s" % datetime.now().time())
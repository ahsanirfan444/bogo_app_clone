from django.core.management.base import BaseCommand
from hubur_apis import models
from datetime import datetime,timedelta


class Command(BaseCommand):
    help = "This command will change the status of stories"

    def handle(self, *args, **options):
        last_24_hours = datetime.now() - timedelta(hours=24)
        models.Story.objects.filter(created_at__lte=last_24_hours).order_by("-created_at").update(is_active=False)
        
        self.stdout.write("Executed at %s" % datetime.now().time())
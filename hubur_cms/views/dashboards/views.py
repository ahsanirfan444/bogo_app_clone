from datetime import datetime
import json
from core.base import AuthBaseViews
from global_methods import AddRewardPoints
from hubur_apis import models
from django.conf import settings
from django.utils.decorators import method_decorator
from core.decorators import vendor_required, admin_required
from django.urls import reverse_lazy
from django.contrib import messages
import notifications

@method_decorator([admin_required], name="dispatch")
class AdminDasboardView(AuthBaseViews):
    TEMPLATE_NAME = "dashboards/admin_dashboard.html"

    def get(self, request, *args, **kwargs):

        return self.render({
            
        })
    
    
@method_decorator([vendor_required], name="dispatch")
class VendorDasboardView(AuthBaseViews):
    TEMPLATE_NAME = "dashboards/vendor_dashboard.html"

    def get(self, request, *args, **kwargs):

        return self.render({
            
        })
    
    def post(self, request, *args, **kwargs):
        voucher_code = request.POST.get('validate_voucher')
        try:
            instance = models.Redemption.objects.get(code=voucher_code, is_redeemed=False, is_expired=False)
            content_instance = models.Content.objects.filter(id=instance.i_content.id, i_business=self.get_vendor_business())
            content_image = models.Images.objects.filter(i_content=instance.i_content)[:1][0]
            
            if content_instance.exists(): 
                instance.is_redeemed = True
                instance.save()

                AddRewardPoints(2, instance.i_user, self.get_vendor_business(), instance.i_content)

                title = instance.i_content.name
                msg = f"you just redeem the offer from {self.get_vendor_business().name}"
                title_ar = instance.i_content.name_ar
                msg_ar = f"أنت فقط تسترد العرض من {self.get_vendor_business().name}"

                notifications.sendNotificationToSingleUser(instance.i_user.id, msg, msg_ar, title, title_ar, request.user.id, instance.i_content.id, 'post_review',notification_type=1, code=None, activityAndroid="FLUTTER_NOTIFICATION_CLICK", activityIOS="FLUTTER_NOTIFICATION_CLICK" , **{"sender": str(self.get_vendor_business().id), "sender_name": str(self.get_vendor_business().name), "content": str(instance.i_content.id), "content_image": str(content_image.image.url), "actions": "post_review" })

                messages.success(request, "Coupon validated successfully")
                return self.redirect(reverse_lazy("vendor_dashboard"))
            else:
                messages.error(request, "In-valid coupon")
                return self.redirect(reverse_lazy("vendor_dashboard"))
            
        except models.Redemption.DoesNotExist:
            messages.error(request, "In-valid coupon")
            return self.redirect(reverse_lazy("vendor_dashboard"))
        
from core.base import AuthBaseViews
from hubur_apis import models
from django.conf import settings
from django.utils.decorators import method_decorator
from core.decorators import vendor_required, admin_required
from django.urls import reverse_lazy
from django.contrib import messages
import notifications
from django.template.loader import render_to_string
from django.db.models import Q

@method_decorator([admin_required], name="dispatch")
class AdminClaimBusinessesList(AuthBaseViews):
    TEMPLATE_NAME = "claim_business/list_all_businesses.html"

    def get(self, request, *args, **kwargs):
        claim_business_list = models.ClaimBusiness.objects.all()

        return self.render({
            'claim_business_list': claim_business_list
        })
    

@method_decorator([admin_required], name="dispatch")
class AdminClaimBusinessesApprove(AuthBaseViews):

    def get(self, request, claim_id, *args, **kwargs):
        try:
            instance = models.ClaimBusiness.objects.get(id=claim_id)
            instance.approve = True
            instance.save()

            models.ClaimBusiness.objects.filter(i_business=instance.i_business).exclude(id=claim_id).delete()

            link = request.build_absolute_uri(reverse_lazy('submit_vendor_profile_details'))+'?place_id='+instance.i_business.place_id

            html_content = render_to_string('includes/emails/approved_claim_business.html', {'business': instance, 'link': link})
       
            notifications.sendEmailToSingleUser(html_content, instance.business_email, 'Your request has approved successfully')

            messages.success(request, self.getCurrentLanguage()['approved_success'])

            return self.redirect(reverse_lazy('list_claim_business'))
        
        except Exception:
            messages.error(request, self.getCurrentLanguage()['something_went_wrong'])
            return self.redirect(reverse_lazy('list_claim_business'))
        

@method_decorator([admin_required], name="dispatch")
class AdminClaimBusinessesReject(AuthBaseViews):

    def get(self, request, claim_id, *args, **kwargs):
        try:
            instance = models.ClaimBusiness.objects.get(id=claim_id)
            instance.delete()

            html_content = render_to_string('includes/emails/reject_claim_business.html', {'business': instance})
       
            notifications.sendEmailToSingleUser(html_content, instance.business_email, 'Your request has been rejected')

            messages.success(request, self.getCurrentLanguage()['rejected_success'])

            return self.redirect(reverse_lazy('list_claim_business'))
        
        except Exception:
            messages.error(request, self.getCurrentLanguage()['something_went_wrong'])
            return self.redirect(reverse_lazy('list_claim_business'))
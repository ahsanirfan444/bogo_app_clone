from django.http import HttpResponseRedirect
from core.base import AuthBaseViews
from hubur_apis import models
from django.conf import settings
from django.utils.decorators import method_decorator
from core.decorators import vendor_required, admin_required
from django.urls import reverse_lazy
from django.contrib import messages
from hubur_cms.forms.subcategory_form import CreateSubCategoryForm
import notifications
from django.template.loader import render_to_string
from django.views.generic import DeleteView

@method_decorator([admin_required], name="dispatch")
class AdminUsersList(AuthBaseViews):
    TEMPLATE_NAME = "users/list_all_users.html"

    def get(self, request, *args, **kwargs):
        interest_list = []
        business_list = []

        all_users = models.UserProfile.objects.filter(role=1)
        all_vendors = models.UserProfile.objects.filter(role=2)

        for users in all_users:
            interest = models.UserInterest.objects.filter(i_user=users)

            interest_list.append(interest)

        all_data = zip(all_users, interest_list)


        for vendors in all_vendors:
            business = models.Business.objects.filter(i_user=vendors)

            business_list.append(business)


        all_business_data = zip(all_vendors, business_list)
        

        return self.render({
            'all_users': all_data,
            'all_vendors': all_business_data
        })
    

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        status = request.POST.get('status')
        status = eval(status)

        models.UserProfile.objects.filter(id=user_id).update(is_active=status)

        if status:
            messages.success(request, "Activated Successfully")
            return self.redirect(reverse_lazy("list_users"))
        else:
            messages.success(request, "De-activated Successfully")
            return self.redirect(reverse_lazy("list_users"))
    

@method_decorator([admin_required], name="dispatch")
class AdminGetVendorProfileOverview(AuthBaseViews):
    TEMPLATE_NAME = "users/vendor_overview.html"

    def get(self, request, vendor_id, *args, **kwargs):
        vendor = models.UserProfile.objects.get(id=vendor_id)
        business_id = models.Business.objects.filter(i_user=vendor).values_list('id', flat=True)
        total_checkins = models.Checkedin.objects.filter(i_business__in=business_id).count()
        
        
        return self.render({
            'vendor': vendor,
            'total_checkins': total_checkins,
        })
    

@method_decorator([admin_required], name="dispatch")
class AdminGetVendorBusinessDetails(AuthBaseViews):
    TEMPLATE_NAME = "users/vendor_business_details.html"

    def get(self, request, vendor_id, *args, **kwargs):
        vendor = models.UserProfile.objects.get(id=vendor_id)
        vendor_business = models.Business.objects.get(i_user=vendor)
        total_checkins = models.Checkedin.objects.filter(i_business=vendor_business).count()

        return self.render({
            'vendor': vendor,
            'vendor_business': vendor_business,
            'total_checkins': total_checkins
        })
    

@method_decorator([admin_required], name="dispatch")
class AdminGetVendorBusinessSchedule(AuthBaseViews):
    TEMPLATE_NAME = "users/vendor_business_schedule.html"

    def get(self, request, vendor_id, *args, **kwargs):
        vendor = models.UserProfile.objects.get(id=vendor_id)
        vendor_business = models.Business.objects.get(i_user=vendor)
        business_schedule = models.BusinessSchedule.objects.filter(i_business=vendor_business).order_by('-i_day')
        total_checkins = models.Checkedin.objects.filter(i_business=vendor_business).count()

        return self.render({
            'vendor': vendor,
            'vendor_business': vendor_business,
            'business_schedule': business_schedule,
            'total_checkins': total_checkins
            
        })
    

@method_decorator([admin_required], name="dispatch")
class AdminGetBusinessCheckInDetails(AuthBaseViews):
    TEMPLATE_NAME = "users/vendor_check_ins.html"

    def get(self, request, vendor_id, *args, **kwargs):
        interest_list = []
        vendor = models.UserProfile.objects.get(id=vendor_id)
        business_id = models.Business.objects.filter(i_user=vendor).values_list('id', flat=True)
        total_checkins = models.Checkedin.objects.filter(i_business__in=business_id).count()
        all_checkins = models.Checkedin.objects.filter(i_business__in=business_id)
        for data in all_checkins:
            interest = models.UserInterest.objects.filter(i_user=data.i_user).values_list('i_category__name', flat=True)
            interest_list.append(interest)

        all_data = zip(all_checkins, interest_list)
        
        return self.render({
            'vendor': vendor,
            'total_checkins': total_checkins,
            'all_data': all_data
        })
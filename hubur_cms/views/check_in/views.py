from django.http import HttpResponseRedirect
from core.base import AuthBaseViews
from hubur_apis import models
from django.conf import settings
from django.utils.decorators import method_decorator
from core.decorators import vendor_required, admin_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DeleteView

@method_decorator([vendor_required], name="dispatch")
class VendorActiveCheckinList(AuthBaseViews):
    TEMPLATE_NAME = "check_in/list_active_check_in.html"

    def get(self, request, *args, **kwargs):
        interest_list = []
        all_checkins = models.Checkedin.objects.filter(i_business=self.get_vendor_business(), is_active=True)
        
        for data in all_checkins:
            interest = models.UserInterest.objects.filter(i_user=data.i_user).values_list('i_category__name', flat=True)
            interest_list.append(interest)

        
        checkin_list = list(zip(all_checkins, interest_list))

        page = request.GET.get('page', 1)
        paginator = Paginator(checkin_list, 9)

        try:
            checkin_list = paginator.page(page)
        except PageNotAnInteger:
            checkin_list = paginator.page(1)
        except EmptyPage:
            checkin_list = paginator.page(paginator.num_pages)

        pagination =  checkin_list

        return self.render({
            'checkin_list': checkin_list,
            'pagination': pagination
        })
    

@method_decorator([vendor_required], name="dispatch")
class VendorInActiveCheckinList(AuthBaseViews):
    TEMPLATE_NAME = "check_in/list_inactive_check_in.html"

    def get(self, request, *args, **kwargs):
        interest_list = []
        all_checkins = models.Checkedin.objects.filter(i_business=self.get_vendor_business(), is_active=False)
        
        for data in all_checkins:
            interest = models.UserInterest.objects.filter(i_user=data.i_user).values_list('i_category__name', flat=True)
            interest_list.append(interest)

        
        inactive_checkin_list = list(zip(all_checkins, interest_list))

        page = request.GET.get('page', 1)
        paginator = Paginator(inactive_checkin_list, 9)

        try:
            inactive_checkin_list = paginator.page(page)
        except PageNotAnInteger:
            inactive_checkin_list = paginator.page(1)
        except EmptyPage:
            inactive_checkin_list = paginator.page(paginator.num_pages)

        pagination =  inactive_checkin_list

        return self.render({
            'inactive_checkin_list': inactive_checkin_list,
            'pagination': pagination
        })
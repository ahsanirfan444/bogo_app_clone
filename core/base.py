from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from constants import SITE_TABS
from datetime import datetime
from hubur_apis import models


class AuthBaseViews(View, LoginRequiredMixin):
    TEMPLATE_NAME = 'base.html'
    SITE_TITLE = "Hubur Way"
    SITE_VERSION = '1.2'
    YEAR = datetime.now().year
    SHOW_SEARCH = False
    CREATE_URL = None
    CREATE_URL_TITLE = None

    def get(self, request, *args, **kwargs):
        raise ValueError("GET method not implemented")

    def post(self, request, *args, **kwargs):
        raise ValueError("POST method not implemented")

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

        if not self.request.user.is_authenticated or not self.request.user.is_active:
            return redirect_to_login(self.request.get_full_path(), reverse_lazy("login_url"))

        return super().dispatch(request, *args, **kwargs)

    def redirect(self, *args):
        """Return a redirect to the given url."""
        return HttpResponseRedirect(*args)
    
    def getNotificationContext(self):
        """Method to get notification context of Admin panel"""
        objects = models.Notification.objects.filter(user=self.request.user, reviewed=False, is_nurse_checkin=False)
        totalUnreviewedNotifications = None
        try:
            notifications = objects[:4]
            totalUnreviewedNotifications = objects.count()
        except IndexError:
            notifications = objects

        returnContext = {
            "notifications": notifications,
            "totalUnreviewedNotifications": totalUnreviewedNotifications
        }
        return returnContext

    def tab_context(self):
        selected_tabs = []

        def getTabs(role, category):
            for tab in SITE_TABS:
                if role in tab['visible'] and (category in tab['visible_categories'] or category == "all"):
                    if self.request.path == str(tab['link_url']):
                        tab['active'] = True
                    elif str(tab['link_url']) == "#":
                        othersTabActive = False
                        for action in tab["actions"]:
                            if self.request.path == str(action['link_url']):
                                action['active'] = True
                                othersTabActive = True
                            else:
                                action['active'] = False
                        
                        if othersTabActive:
                            tab['active'] = True
                        else:
                            tab['active'] = False
                    else:
                        tab['active'] = False
                    selected_tabs.append(tab)

        if self.request.user.is_admin():
            getTabs(role="admin", category='all')
        elif self.request.user.is_vendor():
            try:
                getTabs(role="vendor", category=self.get_vendor_business().i_category.name)
            except Exception:
                getTabs(role="vendor", category='all')

        return selected_tabs
    
    def get_vendor_business(self):
        """Method to get vendor business details"""
        try:
            vendor_business = models.Business.objects.get(i_user=self.request.user)
        except models.Business.DoesNotExist:
            vendor_business = None

        return vendor_business
        
    
    def get_default_context(self):
        new_claim_requests = models.ClaimBusiness.objects.filter(approve=False).count()
        business_id = models.Business.objects.filter(i_user=self.request.user).values_list('id', flat=True)
        total_checkins = models.Checkedin.objects.filter(i_business__in=business_id).count()
        new_booking_requests = models.Booking.objects.filter(status=1, i_business__in=business_id).count()
    
        return {
            'tabs': self.tab_context(),
            'SITE_VERSION': self.SITE_VERSION,
            'YEAR': self.YEAR,
            'SITE_TITLE': self.SITE_TITLE,
            'SHOW_SEARCH': self.SHOW_SEARCH,
            'CREATE_URL': self.CREATE_URL,
            'CREATE_URL_TITLE': self.CREATE_URL_TITLE,
            'new_claim_requests': new_claim_requests,
            'total_checkins': total_checkins,
            'vendor_business': self.get_vendor_business(),
            'new_booking_requests': new_booking_requests
        }

    def render(self, context, **kwargs):
        default_context = self.get_default_context()
        default_context.update(context)


        return render(
            request=self.request,
            template_name=self.TEMPLATE_NAME,
            context=default_context,
            content_type=kwargs.get('content_type', None)
        )


class NonAuthBaseViews(View):
    SITE_TITLE = "Hubur Way"
    SITE_VERSION = '1.2'

    def get(self, request, *args, **kwargs):
        raise ValueError("GET method not implemented")

    def post(self, request, *args, **kwargs):
        raise ValueError("POST method not implemented")

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

        return super().dispatch(request, *args, **kwargs)

    def redirect(self, *args):
        """Return a redirect to the given url."""
        return HttpResponseRedirect(*args)
    

    def get_default_context(self):
        return {
            'SITE_VERSION': self.SITE_VERSION,
            'SITE_TITLE': self.SITE_TITLE,
        }

    def render(self, context, **kwargs):
        default_context = self.get_default_context()
        default_context.update(context)

        return render(
            request=self.request,
            template_name=self.TEMPLATE_NAME,
            context=default_context,
            content_type=kwargs.get('content_type', None)
        )
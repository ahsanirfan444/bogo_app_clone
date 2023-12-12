from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from constants import SITE_TABS
from datetime import datetime
from hubur.settings.base import BASE_DIR
from hubur_apis import models
from django.db.models import Q
import json, os

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
        """Method to get notification context of Admin and Vendor Portal"""
        objects = models.Notification.objects.filter(user=self.request.user)
        totalUnreviewedNotifications = None
        try:
            notifications = objects
            totalUnreviewedNotifications = objects.filter(is_read=False).count()
        except IndexError:
            notifications = objects

        returnContext = {
            "notifications": notifications,
            "totalUnreviewedNotifications": totalUnreviewedNotifications
        }
        return returnContext
    

    def getCurrentLanguage(self):
        """Method to read login user selected language json file"""

        output = None
        if self.request.user.lang_code == 1:
            with open(os.path.join(BASE_DIR, 'locale/en.json'), encoding="utf-8") as file:
                output = json.load(file)
        else:
            with open(os.path.join(BASE_DIR, 'locale/ar.json'), encoding="utf-8-sig") as file:
                output = json.load(file)
        
        return output

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
        new_chats_count = models.Chat.objects.filter((Q(user_1=self.request.user) | Q(user_2=self.request.user)) & Q(is_read=False)).count()
        new_claim_requests = models.ClaimBusiness.objects.filter(approve=False).count()
        business_id = models.Business.objects.filter(i_user=self.request.user).values_list('id', flat=True)
        total_checkins = models.Checkedin.objects.filter(i_business__in=business_id).count()
        new_booking_requests = models.Booking.objects.filter(status=1, i_business__in=business_id).count()
        total_reviews = models.Reviews.objects.filter(i_business__in=business_id).count()
        total_redemptions = models.Redemption.objects.filter(i_content__i_business__in=business_id, is_redeemed=True).count()
        
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
            'total_reviews':total_reviews,
            'total_redemptions':total_redemptions,
            'vendor_business': self.get_vendor_business(),
            'current_language': self.getCurrentLanguage(),
            'new_booking_requests': new_booking_requests,
            'new_chats_count': new_chats_count,
            'server_key': settings.SERVER_KEY,
            'socket_host': settings.SOCKET_HOST
        }

    def render(self, context, **kwargs):
        default_context = self.get_default_context()
        default_context.update(context)

        notifications = self.getNotificationContext()
        default_context.update(notifications)


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
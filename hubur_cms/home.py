import json
from django.http import JsonResponse
from core.base import AuthBaseViews, NonAuthBaseViews
from django.urls import reverse_lazy
from django.contrib.auth import logout
import global_methods
from hubur_apis import models
from push_notifications.models import WebPushDevice

class Home(AuthBaseViews):
    def get(self, request, *args, **kwargs):
        if request.user.is_admin():
            url = reverse_lazy("admin_dashboard")
        elif request.user.is_vendor():
            global_methods.manage_online_status(request.user, True)
            url = reverse_lazy("vendor_dashboard")
        elif request.user.is_superuser():
            url = reverse_lazy("admin:index")
        else:
            url = reverse_lazy("logout_url")
        return self.redirect(url)
    

class RemoveImage(AuthBaseViews):
    def post(self, request, *args, **kwargs):
        image_ids = request.POST.getlist('image_id')
        request.session['image_ids'] = image_ids

        return JsonResponse({'status': True}, safe=False)
    

class SwitchLanguage(AuthBaseViews):
    def get(self, request, *args, **kwargs):
        lang_code = request.GET.get('lang_code')
        request.user.lang_code = lang_code
        request.user.save()
        return self.redirect(request.META.get('HTTP_REFERER'))
    

class LogoutView(NonAuthBaseViews):
    TEMPLATE_NAME = None

    def get(self, request, *args, **kwargs):
        global_methods.manage_online_status(request.user, False)
        wp = WebPushDevice.objects.filter(user_id=request.user.id, active=True)
        wp.update(active=False)
        logout(self.request)
        return self.redirect(reverse_lazy('home'))
    

class RemoveTag(AuthBaseViews):
    def post(self, request, *args, **kwargs):
        tag_id = request.POST.get('tag_id')

        if tag_id:
            models.Tags.objects.filter(id=tag_id).delete()

            response_data = {'success': True}
        else:
            response_data = {'success': False}

        return JsonResponse(response_data)

class ReadNotification(AuthBaseViews):
    def post(self, request, *args, **kwargs):
        notification_id = request.POST.get('notification_id')
        instance = models.Notification.objects.get(id=notification_id)
        instance.is_read = True
        instance.save()

        return JsonResponse({'status': True})
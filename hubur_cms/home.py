from core.base import AuthBaseViews
from django.urls import reverse_lazy

class Home(AuthBaseViews):
    def get(self, request, *args, **kwargs):
        if request.user.is_admin():
            url = reverse_lazy("admin_dashboard")
        elif request.user.is_vendor():
            url = reverse_lazy("vendor_dashboard")
        elif request.user.is_superuser():
            url = reverse_lazy("admin:index")
        else:
            url = reverse_lazy("logout_url")
        return self.redirect(url)
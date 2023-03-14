from core.base import AuthBaseViews
from hubur_apis import models
from django.conf import settings
from django.utils.decorators import method_decorator
from core.decorators import vendor_required, admin_required

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
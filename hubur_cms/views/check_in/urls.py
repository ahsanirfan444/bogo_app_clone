from django.urls import path
from hubur_cms.views.check_in import views

urlpatterns = [
    path("active/", views.VendorActiveCheckinList.as_view(), name="vendor_active_check_in"),
    path("inactive/", views.VendorInActiveCheckinList.as_view(), name="vendor_inactive_check_in")
]
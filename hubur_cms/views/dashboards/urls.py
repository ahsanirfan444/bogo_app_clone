from django.urls import path
from hubur_cms.views.dashboards import views

urlpatterns = [
    path("admin/", views.AdminDasboardView.as_view(), name="admin_dashboard"),
    path("vendor/", views.VendorDasboardView.as_view(), name="vendor_dashboard")
]
from django.urls import path
from hubur_cms.views.visitors import views

urlpatterns = [
    path("all/", views.VendorVisitorsList.as_view(), name="vendor_visitors_list")
]
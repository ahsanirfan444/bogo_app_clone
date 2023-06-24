from django.urls import path
from hubur_cms.views.contents.views.health_care_services import views

urlpatterns = [
    path("all/", views.VendorServicesList.as_view(), name="list_vendor_health_care_services"),
    path("create/", views.VendorCreateServices.as_view(), name="create_health_care_services"),
    path("edit/<content_id>/", views.VendorEditServices.as_view(), name="edit_health_care_services"),
    path("delete/<pk>/", views.VendorDeleteServices.as_view(), name="delete_health_care_services")
]
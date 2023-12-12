from django.urls import path
from hubur_cms.views.web_device_registration import views


urlpatterns = [
    path("web/", views.RegisterWebDevice.as_view()),
]
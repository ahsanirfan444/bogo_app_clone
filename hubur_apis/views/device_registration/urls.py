from push_notifications.api.rest_framework import APNSDeviceAuthorizedViewSet, GCMDeviceAuthorizedViewSet, WebPushDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from hubur_apis.views.device_registration import views

router = DefaultRouter()
router.register('register/ios', APNSDeviceAuthorizedViewSet)
router.register('register/android', GCMDeviceAuthorizedViewSet)


urlpatterns = [
    path("unregister/", views.GCMDeviceAuthorizedAPIView().as_view()),
    path("", include(router.urls))
]
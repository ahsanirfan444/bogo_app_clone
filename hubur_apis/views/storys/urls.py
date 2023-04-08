from django.urls import include, path
from hubur_apis.views.storys import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('business_stories', views.UploadViewSet)

urlpatterns = [

   path('', include(router.urls)),
]

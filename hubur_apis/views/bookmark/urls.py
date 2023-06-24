from django.urls import include, path
from hubur_apis.views.bookmark import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('create', views.MyBookmarkView),
router.register('get', views.MyBookmarkView),

urlpatterns = [

   path('', include(router.urls)),
]

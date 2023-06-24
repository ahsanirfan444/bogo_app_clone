from django.urls import include, path
from hubur_apis.views.visited import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('create', views.MyVisitedView),
router.register('get', views.MyVisitedView),

urlpatterns = [

   path('', include(router.urls)),
]

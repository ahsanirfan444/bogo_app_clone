from django.urls import include, path
from hubur_apis.views.my_rewards import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('get', views.MyRewardListView),

urlpatterns = [

   path('', include(router.urls)),
]

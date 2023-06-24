from django.urls import include, path
from hubur_apis.views.my_favourite import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('create', views.MyFavouriteView),
router.register('get', views.MyFavouriteView),

urlpatterns = [

   path('', include(router.urls)),
]

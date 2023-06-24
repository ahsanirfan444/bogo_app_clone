from django.urls import include, path
from hubur_apis.views.friendlist import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('create', views.FriendListView),
router.register('get', views.FriendListView),

urlpatterns = [

   path('', include(router.urls)),
]

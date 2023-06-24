from django.urls import include, path
from hubur_apis.views.voting import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('create', views.VotingView),
router.register('get', views.VotingView),

urlpatterns = [

   path('', include(router.urls)),
]

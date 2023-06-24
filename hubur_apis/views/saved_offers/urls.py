from django.urls import include, path
from hubur_apis.views.saved_offers import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('create', views.SavedOfferView),
router.register('get', views.SavedOfferView),

urlpatterns = [

   path('', include(router.urls)),
]

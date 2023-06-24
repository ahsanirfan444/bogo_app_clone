from django.urls import include, path
from hubur_apis.views.offers import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('get', views.OfferAPIView)
router.register('get_business_offers', views.GetBusinessOfferAPIView)

urlpatterns = [

   path('', include(router.urls)),
]

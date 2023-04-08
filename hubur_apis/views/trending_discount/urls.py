from django.urls import path,include
from hubur_apis.views.trending_discount import views

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('all', views.TrendingDiscount)
router.register('all_business', views.AllTrendingDiscountBusinesses)

urlpatterns = [
   path('', include(router.urls)),

]

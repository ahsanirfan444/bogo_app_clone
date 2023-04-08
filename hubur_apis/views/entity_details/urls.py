from django.urls import include, path
from hubur_apis.views.entity_details import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('brand', views.BrandsDetailView)
router.register('business', views.BusinessDetailView)

urlpatterns = [

   path('', include(router.urls)),
]

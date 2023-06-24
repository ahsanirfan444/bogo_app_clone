from django.urls import include, path
from hubur_apis.views.entity_details import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('brand', views.BrandsDetailView)
router.register('business', views.BusinessDetailView)
router.register('content', views.ContentDetailView)
router.register('view_all_products', views.ViewAllBusinessProducts)

urlpatterns = [

   path('', include(router.urls)),
]

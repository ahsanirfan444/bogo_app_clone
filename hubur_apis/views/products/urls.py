from django.urls import include, path
from hubur_apis.views.products import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('all', views.ProductsAPIView)

urlpatterns = [

   path('', include(router.urls))

]

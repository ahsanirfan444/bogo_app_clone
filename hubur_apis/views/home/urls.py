from django.urls import path,include
from hubur_apis.views.home import views


from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('all', views.HomeAPIView)  

urlpatterns = [

   path('', include(router.urls)),
]

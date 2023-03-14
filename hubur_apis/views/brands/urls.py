from django.urls import path
from hubur_apis.views.brands import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
   path('all/', views.BrandListAPI.as_view(), name='list_all_brands_view'),
]

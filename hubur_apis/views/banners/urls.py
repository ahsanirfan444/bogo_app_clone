from django.urls import path
from hubur_apis.views.banners import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('topbanners/', views.TopbannerView.as_view(), name='topbanner_view')
]

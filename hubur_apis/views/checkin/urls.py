from django.urls import path
from hubur_apis.views.checkin import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
   path('add/', views.CheckInAPIView.as_view(), name='create_checkin'),

]

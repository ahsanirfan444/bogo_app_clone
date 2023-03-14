from django.urls import path
from hubur_apis.views.storys import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
   # path('add/', views.BrandListAPI.as_view(), name='add_story_view'),
   path('add/', views.UploadViewSet.as_view({'post': 'create'}), name='add_story_view'),

]

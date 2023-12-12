from django.urls import include, path
from hubur_apis.views.campaign import views


urlpatterns = [
   path('get/', views.CampaignAPIView.as_view(), name='get-campaign'),
]

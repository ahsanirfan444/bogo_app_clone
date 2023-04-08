from django.urls import path
from hubur_apis.views.business import views



urlpatterns = [
   path('claim/', views.ClaimBusinessAPIView.as_view(), name='claim_business_view_api'),
   path('getbusiness/', views.GetAllBususiness.as_view({'get': 'list'}), name='claim_business_view_api'),

]

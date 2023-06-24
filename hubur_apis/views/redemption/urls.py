from django.urls import path
from hubur_apis.views.redemption import views



urlpatterns = [
   path('create_code/', views.CreateRedemptionCodeAPIView.as_view(), name='create_redemption_view_api'),
   path('create_redemption/', views.RedemptionAPIView.as_view(), name='create_redemption_view_api'),

]

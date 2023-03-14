from django.urls import path,include
from hubur_apis.views.interest import views


urlpatterns = [
   path('user_interest/', views.CreateUserInterestAPIView.as_view(), name='user_interest_view_api'),
   path('get_catagories/', views.GetCatagoriesListAPIView.as_view(), name='get_all_catagories_view'),

]

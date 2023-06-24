from django.urls import path
from hubur_apis.views.checkin import views


urlpatterns = [
   path('add/', views.CheckInAPIView.as_view({'post': 'create'}), name='create_checkin'),
   path('get/', views.CheckInAPIView.as_view({'get': 'list'}), name='get_checkin'),

]

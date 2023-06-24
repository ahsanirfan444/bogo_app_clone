from django.urls import include, path
from hubur_apis.views.notification import views


urlpatterns = [

   path('get/', views.GetNotificationAPIView.as_view()),
   path('read/', views.ReadNotificationAPIView.as_view())
]

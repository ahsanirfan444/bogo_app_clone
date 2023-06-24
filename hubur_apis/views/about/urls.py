from django.urls import path
from hubur_apis.views.about import views


urlpatterns = [

   path('about_us/',views.AboutUsAPIView.as_view()),
   path('terms_and_policy/',views.OtherAPIView.as_view()),
   path('contact_us/',views.OtherAPIView.as_view()),
   path('get_contact_us/',views.ContactUsAPIView.as_view()),
   
]

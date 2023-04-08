from django.urls import path
from hubur_cms.views.businesses import views

urlpatterns = [
    path("all/", views.AdminBusinessesList.as_view(), name="list_all_businesses")
]
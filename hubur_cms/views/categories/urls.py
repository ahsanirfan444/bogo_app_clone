from django.urls import path
from hubur_cms.views.categories import views

urlpatterns = [
    path("all/", views.AdminCategoriesList.as_view(), name="list_categories")
]
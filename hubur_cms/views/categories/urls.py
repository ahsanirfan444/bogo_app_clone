from django.urls import path
from hubur_cms.views.categories import views

urlpatterns = [
    path("all/", views.AdminCategoriesList.as_view(), name="list_categories"),
    path("edit/<cat_id>/", views.AdminEditCategoriesView.as_view(), name="edit_category"),
]
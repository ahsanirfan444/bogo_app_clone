from django.urls import path
from hubur_cms.views.sub_categories import views

urlpatterns = [
    path("all/", views.AdminSubCategoriesList.as_view(), name="list_sub_categories"),
    path("create/", views.AdminCreateSubCategoriesView.as_view(), name="create_sub_category"),
    path("edit/<sub_cat_id>/", views.AdminEditSubCategoriesView.as_view(), name="edit_sub_category"),
    path("delete/<pk>/", views.AdminDeleteSubCategoriesView.as_view(), name="delete_sub_category")
]
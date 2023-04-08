from django.urls import path
from hubur_cms.views.brands import views

urlpatterns = [
    path("all/", views.AdminBrandsList.as_view(), name="list_brands"),
    path("create/", views.AdminCreateBrandsView.as_view(), name="create_brands"),
    path("edit/<brand_id>/", views.AdminEditBrandsView.as_view(), name="edit_brands"),
    path("delete/<pk>/", views.AdminDeleteBrandsView.as_view(), name="delete_brands")
]
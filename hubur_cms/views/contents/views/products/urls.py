from django.urls import path
from hubur_cms.views.contents.views.products import views

urlpatterns = [
    path("all/", views.VendorProductsList.as_view(), name="list_vendor_products"),
    path("create/", views.VendorCreateProducts.as_view(), name="create_products"),
    path("edit/<content_id>/", views.VendorEditProducts.as_view(), name="edit_products"),
    path("delete/<pk>/", views.VendorDeleteProducts.as_view(), name="delete_products")
]
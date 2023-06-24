from django.urls import path
from hubur_cms.views.contents.views.menus import views

urlpatterns = [
    path("all/", views.VendorMenuList.as_view(), name="list_vendor_menus"),
    path("create/", views.VendorCreateMenu.as_view(), name="create_menu"),
    path("edit/<content_id>/", views.VendorEditMenu.as_view(), name="edit_menu"),
    path("delete/<pk>/", views.VendorDeleteMenu.as_view(), name="delete_menu")
]
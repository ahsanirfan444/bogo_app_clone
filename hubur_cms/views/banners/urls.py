from django.urls import path
from hubur_cms.views.banners import views

urlpatterns = [
    path("all/", views.AdminBannersList.as_view(), name="list_banners"),
    path("create/", views.AdminCreateBannersView.as_view(), name="create_banners"),
    path("edit/<ban_id>/", views.AdminEditBannersView.as_view(), name="edit_banners"),
    path("delete/<pk>/", views.AdminDeleteBannersView.as_view(), name="delete_banners")
]
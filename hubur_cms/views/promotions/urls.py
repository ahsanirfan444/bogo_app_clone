from django.urls import path
from hubur_cms.views.promotions import views

urlpatterns = [
    path("all/", views.AdminPromotionsList.as_view(), name="list_promotions"),
    path("create/", views.AdminCreatePromotionsView.as_view(), name="create_promotion"),
    path("edit/<promo_id>/", views.AdminEditPromotionsView.as_view(), name="edit_promotion"),
    path("delete/<pk>/", views.AdminDeletePromotionsView.as_view(), name="delete_promotion")
]
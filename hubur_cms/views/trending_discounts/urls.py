from django.urls import path
from hubur_cms.views.trending_discounts import views

urlpatterns = [
    path("all/", views.AdminTrendingDiscountsList.as_view(), name="list_trending_discounts"),
    path("create/", views.AdminCreateTrendingDiscountsView.as_view(), name="create_trending_discounts"),
    path("edit/<discount_id>/", views.AdminEditTrendingDiscountsView.as_view(), name="edit_trending_discounts"),
    path("delete/<pk>/", views.AdminDeleteTrendingDiscountsView.as_view(), name="delete_trending_discounts")
]
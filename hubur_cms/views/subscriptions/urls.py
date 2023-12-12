from django.urls import path
from hubur_cms.views.subscriptions import views

urlpatterns = [
    path("all/", views.AdminSubscriptionList.as_view(), name="list_subscriptions"),
    path("create/", views.AdminCreateSubscriptionView.as_view(), name="create_subscription"),
    path("edit/<sub_id>/", views.AdminEditSubscriptionView.as_view(), name="edit_subscription"),
    path("delete/<pk>/", views.AdminDeleteSubscriptionView.as_view(), name="delete_subscription")
]
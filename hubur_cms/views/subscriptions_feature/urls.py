from django.urls import path
from hubur_cms.views.subscriptions_feature import views

urlpatterns = [
    path("all/<sub_id>/", views.AdminSubscriptionFeatureList.as_view(), name="list_subscriptions_feature"),
    path("create/<sub_id>/", views.AdminCreateSubscriptionFeatureView.as_view(), name="create_subscription_feature"),
    path("edit/<sub_id>/<feature_id>/", views.AdminEditSubscriptionFeatureView.as_view(), name="edit_subscription_feature"),
    path("delete/<pk>/", views.AdminDeleteSubscriptionFeatureView.as_view(), name="delete_subscription_feature")
]
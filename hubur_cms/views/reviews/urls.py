from django.urls import path
from hubur_cms.views.reviews import views

urlpatterns = [
    path("get-reviews/", views.VendorReviewsList.as_view(), name="vendor_reviews"),
]
from django.urls import path
from hubur_cms.views.vendor_onboarding import views

urlpatterns = [
    path("profile-details/", views.SubmitVendorProfileDetails.as_view(), name="submit_vendor_profile_details"),
    path("profile-verify/", views.VerifyVendorProfileDetails.as_view(), name="verify_vendor_profile_details"),
    path("business-details/", views.SubmitVendorBusinessDetails.as_view(), name="submit_vendor_business_details"),
    path("business-schedule/", views.SubmitVendorBusinessSchedule.as_view(), name="submit_vendor_business_schedule"),
    path("done/", views.VendorOnboardingCompleted.as_view(), name="vendor_onboarding_completed"),
    path("fetch-subCategories/", views.FetchSubCategories.as_view(), name="fetch_subcategories")
]
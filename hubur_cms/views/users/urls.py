from django.urls import path
from hubur_cms.views.users import views

urlpatterns = [
    path("all/", views.AdminUsersList.as_view(), name="list_users"),
    path("profile/<vendor_id>/", views.AdminGetVendorProfileOverview.as_view(), name="vendor_profile_overview"),
    path("business-details/<vendor_id>/", views.AdminGetVendorBusinessDetails.as_view(), name="vendor_business_details"),
    path("business-schedule/<vendor_id>/", views.AdminGetVendorBusinessSchedule.as_view(), name="vendor_business_schedule"),
    path("checkin-details/<vendor_id>/", views.AdminGetBusinessCheckInDetails.as_view(), name="vendor_business_checkin_details"),
]
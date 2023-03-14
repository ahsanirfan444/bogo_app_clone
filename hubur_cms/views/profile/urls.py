from django.urls import path
from hubur_cms.views.profile import views

urlpatterns = [
    path("overview/", views.ProfileOverview.as_view(), name="profile_overview"),
    path("edit-profile-details/", views.EditProfileDetails.as_view(), name="edit_profile_details"),
    path("business-details/", views.BusinessDetails.as_view(), name="business_details"),
    path("edit-business-details/", views.EditBusinessDetails.as_view(), name="edit_business_details"),
    path("business-schedule/", views.BusinessSchedule.as_view(), name="business_schedule"),
    path("edit-business-schedule/", views.EditBusinessSchedule.as_view(), name="edit_business_schedule")
]
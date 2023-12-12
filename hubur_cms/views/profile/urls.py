from django.urls import path
from hubur_cms.views.profile import views

urlpatterns = [
    path("overview/", views.ProfileOverview.as_view(), name="profile_overview"),
    path("edit-profile-details/", views.EditProfileDetails.as_view(), name="edit_profile_details"),
    path("business-details/", views.BusinessDetails.as_view(), name="business_details"),
    path("edit-business-details/", views.EditBusinessDetails.as_view(), name="edit_business_details"),
    path("business-schedule/", views.BusinessSchedule.as_view(), name="business_schedule"),
    path("edit-business-schedule/", views.EditBusinessSchedule.as_view(), name="edit_business_schedule"),
    path("business-catalogue/", views.BusinessCatalogueDetails.as_view(), name="business_catalogue"),
    path("create-business-catalogue/", views.CreateBusinessCatalogue.as_view(), name="create_business_catalogue"),
    path("edit-business-catalogue/<cat_id>/", views.EditBusinessCatalogue.as_view(), name="edit_business_catalogue"),
    path("delete-business-catalogue/<pk>/", views.DeleteBusinessCatalogue.as_view(), name="delete_business_catalogue"),
    path("settings/", views.ProfileSettings.as_view(), name="profile_settings"),
    path("edit-contact-settings/", views.EditProfileContactSettings.as_view(), name="edit_profile_contact_settings"),
    path("change-password/", views.ChangePassword.as_view(), name="change_password"),
    path("subscription-plans/", views.SubscriptionPlans.as_view(), name="subscription_plans")
]
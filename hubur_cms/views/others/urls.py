from django.urls import path
from hubur_cms.views.others import views

urlpatterns = [
    path("faq/", views.FAQView.as_view(), name="others_faq"),
    path("edit/faq/<faq_id>/", views.EditFAQView.as_view(), name="edit_faq"),
    path("delete/faq/<pk>/", views.DeleteFAQView.as_view(), name="delete_faq"),
    path("terms-conditions/", views.TermsAndConditionView.as_view(), name="others_terms_and_condition"),
    path("about-us/", views.AboutUsView.as_view(), name="others_about_us"),
    path("privacy-policy/", views.PrivacyPolicyView.as_view(), name="others_privacy_policy"),
    path("disclaimer/", views.DisclaimerView.as_view(), name="others_disclaimer")
]
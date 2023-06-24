from django.urls import path
from hubur_cms.views.stories import views

urlpatterns = [
    path("active/", views.VendorActiveStoriesList.as_view(), name="vendor_active_stories"),
    path("inactive/", views.VendorInActiveStoriesList.as_view(), name="vendor_inactive_stories"),
    path("deactivate/<story_id>/", views.VendorsDeActivateStoriesView.as_view(), name="vendor_deactivate_stories"),
    path("delete/<pk>/", views.VendorsDeleteStoriesView.as_view(), name="vendor_delete_stories")
]
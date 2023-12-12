from django.urls import path
from hubur_cms.views.businesses import views

urlpatterns = [
    path("all/", views.AdminBusinessesList.as_view(), name="list_all_businesses"),
    path("business-detail/<int:pk>/", views.AdminBusinessDetail.as_view(), name="business_detail_by_admin"),
    path("edit-business-details/<int:pk>/", views.EditBusinessDetailsByAdmin.as_view(), name="edit_business_details_by_admin"),
    path("business-Schedule/<int:pk>/", views.AdminBusinessSchedule.as_view(), name="business_schedule_by_admin"),
    path("edit-business-Schedule/<int:pk>/", views.EditBusinessScheduleByAdmin.as_view(), name="edit_business_schedule_by_admin"),
    path("business-catalogue/<int:pk>/", views.AdminBusinessCatalogueDetails.as_view(), name="business_catalogue_by_admin"),
    path("business-active-stories/<int:pk>/", views.AdminBusinessActiveStoriesList.as_view(), name="business_active_stories_by_admin"),
    path("business-inactive-stories/<int:pk>/", views.AdminBusinessInActiveStoriesList.as_view(), name="business_inactive_stories_by_admin"),
    path("deactivate-by-admin/<int:pk>/<int:business_id>/", views.DeActivateStoriesByAdminView.as_view(), name="deactivate_stories_by_admin"),
    path("delete-stories-by-admin/<int:pk>/<int:business_id>/<str:is_active>/", views.DeleteStoriesByAdminView.as_view(), name="delete_stories_by_admin"),
    path("business-reviews/<int:pk>/", views.AdminBusinessReviews.as_view(), name="business_reviews_by_admin"),
    path("delete-rating-by-admin/<int:pk>/<int:business_id>/", views.DeleteReviewByAdminView.as_view(), name="delete_ratings_by_admin"),
    path("subscription-plans/<int:pk>/", views.SubscriptionPlansByAdmin.as_view(), name="subscription_plans_by_admin"),
    path("create-business-catalogue/<int:business_id>/", views.CreateBusinessCatalogueByAdmin.as_view(), name="create_business_catalogue_by_admin"),
    path("edit-business-catalogue-by-admin/<cat_id>/<int:business_id>/", views.EditBusinessCatalogueByAdmin.as_view(), name="edit_business_catalogue_by_admin"),
    path("delete-business-catalogue-by-admin/<cat_id>/<int:business_id>/", views.DeleteCatalogueByAdminView.as_view(), name="delete_business_catalogue_by_admin"),
    
    
]
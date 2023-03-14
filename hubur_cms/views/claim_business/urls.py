from django.urls import path
from hubur_cms.views.claim_business import views

urlpatterns = [
    path("all/", views.AdminClaimBusinessesList.as_view(), name="list_claim_business"),
    path("approve/<claim_id>/", views.AdminClaimBusinessesApprove.as_view(), name="approve_claim_business"),
    path("reject/<claim_id>/", views.AdminClaimBusinessesReject.as_view(), name="reject_claim_business")
]
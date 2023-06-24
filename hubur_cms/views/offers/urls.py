from django.urls import path
from hubur_cms.views.offers import views

urlpatterns = [
    path("all/", views.VendorOffersList.as_view(), name="list_vendor_offers"),
    path("create/", views.VendorCreateOffer.as_view(), name="create_offer"),
    path("edit/<offer_id>/", views.VendorEditOffer.as_view(), name="edit_offer"),
    path("delete/<pk>/", views.VendorDeleteOffer.as_view(), name="delete_offer")
]
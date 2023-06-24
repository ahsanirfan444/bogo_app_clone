from django.urls import path
from hubur_cms.views.bookings import views

urlpatterns = [
    path("all/", views.VendorBookingsView.as_view(), name="list_vendor_bookings"),
    path("accept/<book_id>/", views.VendorBookingAcceptView.as_view(), name="accept_booking"),
    path("cancel/<book_id>/", views.VendorBookingCancelView.as_view(), name="cancel_booking")
]
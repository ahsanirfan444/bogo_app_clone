from django.urls import path
from hubur_cms.views.votes import views

urlpatterns = [
    path("like/", views.VendorVotesList.as_view(), name="vendor_votes"),
    path("dislike/", views.VendorUnVotesList.as_view(), name="vendor_un_votes")
]
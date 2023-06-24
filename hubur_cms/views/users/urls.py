from django.urls import path
from hubur_cms.views.users import views

urlpatterns = [
    path("all/", views.AdminUsersList.as_view(), name="list_users")
]
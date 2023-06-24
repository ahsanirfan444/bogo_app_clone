from django.urls import path, include
from hubur_cms.views.contents import views

urlpatterns = [
    path("product/", include("hubur_cms.views.contents.views.products.urls")),
    path("service/", include("hubur_cms.views.contents.views.services.urls")),
    path("health-care-service/", include("hubur_cms.views.contents.views.health_care_services.urls")),
    path("menu/", include("hubur_cms.views.contents.views.menus.urls"))
]
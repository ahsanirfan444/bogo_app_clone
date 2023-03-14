from django.urls import path, include
from django.contrib.auth.decorators import login_required

# Create your views here.

urlpatterns = [
    path("user/", include('hubur_apis.views.user.urls')),
    path("banners/", include('hubur_apis.views.banners.urls')),
    path("brands/", include('hubur_apis.views.brands.urls')),
    path("storys/", include('hubur_apis.views.storys.urls')),
    path("checkin/", include('hubur_apis.views.checkin.urls')),
    path("products/", include('hubur_apis.views.products.urls')),
    path("business/", include('hubur_apis.views.business.urls')),
    path("redemption/", include('hubur_apis.views.redemption.urls')),
    path("overall_search/", include('hubur_apis.views.search.urls')),
    path("interest/", include('hubur_apis.views.interest.urls')),
    path("home/", include('hubur_apis.views.home.urls')),
]

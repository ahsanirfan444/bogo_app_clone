from django.urls import path, include
from django.contrib.auth.decorators import login_required

# Create your views here.

urlpatterns = [
    path("user/", include('hubur_apis.views.user.urls')),
    path("brands/", include('hubur_apis.views.brands.urls')),
    path("storys/", include('hubur_apis.views.storys.urls')),
    path("checkin/", include('hubur_apis.views.checkin.urls')),
    path("products/", include('hubur_apis.views.products.urls')),
    path("business/", include('hubur_apis.views.business.urls')),
    path("redemption/", include('hubur_apis.views.redemption.urls')),
    path("overall_search/", include('hubur_apis.views.search.urls')),
    path("interest/", include('hubur_apis.views.interest.urls')),
    path("home/", include('hubur_apis.views.home.urls')),
    path("detail/", include('hubur_apis.views.entity_details.urls')),
    path("trending_discount/", include('hubur_apis.views.trending_discount.urls')),
    path("socket/", include('hubur_apis.views.socket.urls')),
    path("voting/", include('hubur_apis.views.voting.urls')),
    path("my_favourite/", include('hubur_apis.views.my_favourite.urls')),
    path("visited/", include('hubur_apis.views.visited.urls')),
    path("about/", include('hubur_apis.views.about.urls')),
    path("book_a_table/", include('hubur_apis.views.book_a_table.urls')),
    path("my_bookmark/", include('hubur_apis.views.bookmark.urls')),
    path("offers/", include('hubur_apis.views.offers.urls')),
    path("reviews/", include('hubur_apis.views.reviews.urls')),
    path("saved_offers/", include('hubur_apis.views.saved_offers.urls')),
    path("notification_detail/", include('hubur_apis.views.notification.urls')),
    path("friend_list/", include('hubur_apis.views.friendlist.urls')),
    path("my_rewards/", include('hubur_apis.views.my_rewards.urls')),
    path("chat/", include('hubur_apis.views.chat.urls')),
    path("campaign/", include('hubur_apis.views.campaign.urls')),

    # Device registration URLs
    path("device/", include("hubur_apis.views.device_registration.urls"))
]

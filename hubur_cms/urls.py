from django.urls import path, include
from core.decorators import guest_required
from hubur_cms import home
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Auth Views
    path('auth/login/', auth_views.LoginView.as_view(template_name='login.html', extra_context={'hide_title': True}), name='login_url'),
    path('auth/logout/', auth_views.LogoutView.as_view(template_name='logout.html', extra_context={'hide_title': True}), name='logout_url'),

    # Home View
    path("", home.Home.as_view(), name="home"),

    # Vendor onboarding urls
    path("register/", include("hubur_cms.views.vendor_onboarding.urls")),
    
    # Reset password urls    
    path('reset/password/', guest_required(auth_views.PasswordResetView.as_view(template_name='forgot_password/password-change-request.html', html_email_template_name='includes/emails/password_reset_email.html', extra_context={'hide_title': True})), name='password_reset'),   
    path('reset/password/done', guest_required(auth_views.PasswordResetDoneView.as_view(template_name='forgot_password/password_reset_done.html', extra_context={'hide_title': True})), name='password_reset_done'),    
    path('reset/<uidb64>/<token>/', guest_required(auth_views.PasswordResetConfirmView.as_view(template_name='forgot_password/confirm_email.html', extra_context={'hide_title': True})), name='password_reset_confirm'),    
    path('reset/done/', guest_required(auth_views.PasswordResetCompleteView.as_view(template_name='forgot_password/completion_msg.html', extra_context={'hide_title': True})), name='password_reset_complete'),

    # profile urls
    path("profile/", include("hubur_cms.views.profile.urls")),

    # Dasboards Urls
    path("dashboard/", include("hubur_cms.views.dashboards.urls")),

    # Claim Businesses Urls
    path("claim-business/", include("hubur_cms.views.claim_business.urls")),

    # Categories Urls
    path("categories/", include("hubur_cms.views.categories.urls")),

    # Sub Categories Urls
    path("sub-categories/", include("hubur_cms.views.sub_categories.urls")),

    # Banners
    path("banners/", include("hubur_cms.views.banners.urls")),

    # Brands
    path("brands/", include("hubur_cms.views.brands.urls")),

    # Users
    path("users/", include("hubur_cms.views.users.urls")),
    
    # businesses
    path("businesses/", include("hubur_cms.views.businesses.urls")),

    # trending discounts
    path("trending-discounts/", include("hubur_cms.views.trending_discounts.urls")),

    # stories
    path("stories/", include("hubur_cms.views.stories.urls")),

    # checkin
    path("check-in/", include("hubur_cms.views.check_in.urls")),

    # voting
    path("voting/", include("hubur_cms.views.votes.urls")),

    # visitors
    path("visitors/", include("hubur_cms.views.visitors.urls")),

    # others
    path("get/", include("hubur_cms.views.others.urls")),

    # Bookings
    path("bookings/", include("hubur_cms.views.bookings.urls")),

    # Content
    path("content/", include("hubur_cms.views.contents.urls")),

    # Offers
    path("offers/", include("hubur_cms.views.offers.urls")),

    # ajax urls
    path("remove_image/", home.RemoveImage.as_view(), name="remove_image"),
]
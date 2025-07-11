from django.urls import path, include
from django.urls.conf import re_path
from hubur_apis.views.user import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('create_user', views.UserProfileViewSet)
router.register('get_cities', views.GetAllCitiesViewSet)
router.register('get_countries', views.GetAllCitiesViewSet)

urlpatterns = [
    path('api_token_auth/', views.CustomAuthLogin.as_view(), name='api-token-auth/'),
    path('change_notification_settings/', views.ChangeNotificationSettingAPIView.as_view(), name='change-notification-settings/'),
    path('apple_login/', views.AppleLoginAPIView.as_view(), name='apple-login/'),
    path('verify_user/', views.VerifyUser.as_view(), name='verify-password'),
    path('reset_password/', views.ResetPassword.as_view(), name='reset_password'),
    path('forgot_password/', views.ForgotPassword.as_view(), name='forgot-password'),
    path('resend_code/', views.ResendCodeAPI.as_view(), name='resend-code'),
    path('change_pass_after_verify/', views.ChangePassAfterVerify.as_view(), name='change-pass-after-verify'),
    path('save_location/', views.SaveLocatonView.as_view(), name='save-location'),
    path('status/<int:pk>', views.UserStatusAPIView.as_view()),
    path('status/', views.UserStatusTokenAPIView.as_view()),
    path('change_online_status/', views.UserOnlineStatusAPIView.as_view()),
    path('', include(router.urls))
]

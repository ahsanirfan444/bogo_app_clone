from django.urls import path, include
from django.urls.conf import re_path
from hubur_apis.views.user import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('create_user', views.UserProfileViewSet)

urlpatterns = [
    path('api_token_auth/', views.CustomAuthLogin.as_view(), name='api-token-auth/'),
    path('verify_user/', views.VerifyUser.as_view(), name='verify-password'),
    path('reset_password/', views.ResetPassword.as_view(), name='reset_password'),
    path('forgot_password/', views.ForgotPassword.as_view(), name='forgot-password'),
    path('resend_code/', views.ResendCodeAPI.as_view(), name='resend-code'),
    path('change_pass_after_verify/', views.ChangePassAfterVerify.as_view(), name='change-pass-after-verify'),
    path('save_location/', views.SaveLocatonView.as_view(), name='change-pass-after-verify'),
    path('status/', views.UserStatusAPIView.as_view()),
    path('', include(router.urls))
]

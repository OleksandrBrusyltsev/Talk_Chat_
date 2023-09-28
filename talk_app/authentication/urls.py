from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import EmailLoginAPIView, UserRegistrationAPIView, confirm_account, \
    PasswordResetAPIView, PasswordResetConfirmAPIView

urlpatterns = [
    path('login/', EmailLoginAPIView.as_view(), name='email-login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('confirm/<int:user_id>/', confirm_account, name='confirm-account'),
    path('password_reset/', PasswordResetAPIView.as_view(), name='password-reset'),
    path('password_reset_confirm/', PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm'), ]

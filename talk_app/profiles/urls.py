
from django.urls import path

from profiles.views import RefreshUser, ProfileUpdateView
from profiles.views import DeleteAccountView, ChangePasswordView

urlpatterns = [
    path('refresh_user/', RefreshUser.as_view(), name='refresh-user'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('delete_account/', DeleteAccountView.as_view(), name='delete-account'),
    path('profile_update/', ProfileUpdateView.as_view(), name='profile_update'),
]
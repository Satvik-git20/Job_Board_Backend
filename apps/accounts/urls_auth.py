from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    ChangePasswordView,
    VerifyEmailView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='auth_login'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('refresh-token/', TokenRefreshView.as_view(), name='auth_refresh_token'),
    path('change-password/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('verify-email/', VerifyEmailView.as_view(), name='auth_verify_email'),
]

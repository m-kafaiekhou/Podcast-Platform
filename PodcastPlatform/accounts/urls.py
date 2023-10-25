from django.contrib import admin
from django.urls import path

from .views import (
    LoginView,
    RefreshTokenView,
    RegisterView,
    AuthenticatedView,
    LogoutView,
    ResetPasswordView,
    ForgotPasswordView,
)

app_name = 'accounts'

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),
    path('register/', RegisterView.as_view(), name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('test-auth/', AuthenticatedView.as_view(), name="test-auth"),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),

]

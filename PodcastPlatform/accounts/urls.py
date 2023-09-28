from django.contrib import admin
from django.urls import path

from .views import (
    LoginView,
    RefreshTokenView,
    RegisterView,
    AuthenticatedView,
    LogoutView,
)

app_name = 'accounts'

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),
    path('register/', RegisterView.as_view(), name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('test-auth/', AuthenticatedView.as_view(), name="test-auth"),
]

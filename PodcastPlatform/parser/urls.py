from django.urls import path, include

from .views import ParseView

app_name = 'parser'

urlpatterns = [
    path("parse/", ParseView.as_view(), name="parse"),
]

from django.urls import path

from .api.login import LoginAPI
from .api.register import RegisterAPI

urlpatterns = [
    path(
        "api/auth/register/",
        RegisterAPI.as_view(),
        name="api_auth_register"
    ),
    path(
        "api/auth/login/",
        LoginAPI.as_view(),
        name="api_auth_login"
    ),
]

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path("auth/user/new/", views.UserCreateAPIView.as_view()),
    path("auth/get-token/", obtain_auth_token, name="api_token_auth"),
]

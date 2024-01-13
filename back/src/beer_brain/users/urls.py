from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path("get-token/", obtain_auth_token),
    path("new/", views.UserCreateAPIView.as_view()),
    path("profile/me/", views.SelfUserAPIView.as_view()),
    path("profile/<str:username>/", views.UserGetAPIView.as_view()),
]

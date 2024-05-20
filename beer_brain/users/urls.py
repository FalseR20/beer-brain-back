from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path("token/", obtain_auth_token, name="get-token"),
    path("new/", views.UserCreateAPIView.as_view(), name="create-user"),
    path("me/", views.SelfUserAPIView.as_view(), name="get-my-user"),
    path("me/change-password/", views.ChangePasswordAPIView.as_view(), name="change-password"),
    path("id/<int:pk>/", views.UserGetAPIView.as_view(), name="get-user"),
    path(
        "username/<str:username>/",
        views.UserGetByUsernameAPIView.as_view(),
        name="get-user-by-username",
    ),
]

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path("auth/user/new/", views.UserCreateAPIView.as_view()),
    path("auth/get-token/", obtain_auth_token, name="api_token_auth"),
    path("core/events/all/", views.EventListAPIView.as_view()),
    path("core/events/new/", views.EventCreateAPIView.as_view()),
    path("core/events/<int:event_id>/join/", views.MemberAPIView.as_view()),
    path("core/events/<int:pk>/", views.EventRetrieveUpdateAPIView.as_view()),
    path("core/full-events/<int:pk>/", views.FullEventRetrieveUpdateAPIView.as_view()),
]

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path("auth/register/", views.UserViewSet.as_view({"post": "create"})),
    path("auth/token/", obtain_auth_token, name="api_token_auth"),
    path("core/common-events/", views.EventsAPIView.as_view(), name="common-events"),
    path("core/create-event/", views.CreateEventViewSet.as_view(), name="create-event"),
    path("core/events/<int:pk>/", views.GetEventFull.as_view(), name="get-event"),
]

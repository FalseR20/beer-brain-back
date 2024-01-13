from django.urls import path

from . import views

urlpatterns = [
    path("", views.EventListAPIView.as_view()),
    path("new/", views.EventCreateAPIView.as_view()),
    path("<str:pk>/", views.EventRetrieveUpdateAPIView.as_view()),
    path("<str:pk>/join/", views.join_event_api_view),
    path("<str:pk>/leave/", views.leave_event_api_view),
    path("detailed/<str:pk>/", views.FullEventRetrieveUpdateAPIView.as_view()),
]

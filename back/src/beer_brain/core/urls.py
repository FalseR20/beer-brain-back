from django.urls import path

from . import views

urlpatterns = [
    path("events/all/", views.EventListAPIView.as_view()),
    path("events/new/", views.EventCreateAPIView.as_view()),
    path("events/<int:event_id>/join/", views.MemberAPIView.as_view()),
    path("events/<int:pk>/", views.EventRetrieveUpdateAPIView.as_view()),
    path("full-events/<int:pk>/", views.FullEventRetrieveUpdateAPIView.as_view()),
]

from django.urls import path

from . import views


urlpatterns = [
    path("common-events/", views.EventsAPIView.as_view(), name="common-events"),
    path("new-event/", views.NewEventViewSet.as_view({"post": "create"}), name="new-event"),
]

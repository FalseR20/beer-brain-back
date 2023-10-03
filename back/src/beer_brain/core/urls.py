from django.urls import path

from . import views


urlpatterns = [
    path("common-events/", views.EventsAPIView.as_view(), name="common-events"),
    path("create-event/", views.CreateEventViewSet.as_view({"post": "create"}), name="create-event"),
]

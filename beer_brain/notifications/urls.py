from django.urls import path

from . import views

urlpatterns = [
    path("", views.NotificationListView.as_view(), name="get-notifications"),
    path("unread/", views.UnreadNotificationListView.as_view(), name="get-unread-notifications"),
    path(
        "mark-read/<int:pk>/",
        views.MarkNotificationsView.as_view(),
        name="mark-notifications",
    ),
]

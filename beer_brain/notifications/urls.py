from django.urls import path

from . import views

urlpatterns = [
    path("", views.NotificationListView.as_view(), name="get-notifications"),
    path("<int:pk>/", views.NotificationAPIView.as_view(), name="ru-notification"),
]

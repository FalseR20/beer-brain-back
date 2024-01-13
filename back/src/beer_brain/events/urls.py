from django.urls import path

from . import views

urlpatterns = [
    path("new/", views.EventCreateAPIView.as_view()),
    # path("/", views.EventListAPIView.as_view()),
    path("<str:pk>/", views.EventRetrieveUpdateAPIView.as_view()),
    # path("<int:event_id>/join/", views.MemberAPIView.as_view()),
    path("detailed/<str:pk>/", views.FullEventRetrieveUpdateAPIView.as_view()),
]

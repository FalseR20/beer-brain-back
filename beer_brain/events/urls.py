from django.urls import path

from . import views

urlpatterns = [
    path("", views.EventListAPIView.as_view(), name="event-list"),
    path("new/", views.EventCreateAPIView.as_view(), name="create-event"),
    path("<uuid:pk>/", views.EventRetrieveUpdateDestroyAPIView.as_view(), name="rud-event"),
    path("<uuid:pk>/join/", views.join_event_api_view, name="join-event"),
    path("<uuid:pk>/leave/", views.leave_event_api_view, name="leave-event"),
    path("<uuid:pk>/change-host/", views.ChangeHostAPIView.as_view(), name="change-host"),
    path(
        "<uuid:pk>/detailed/",
        views.DetailedEventRetrieveAPIView.as_view(),
        name="get-detailed-event",
    ),
    path("<uuid:event_id>/deposits/", views.DepositListAPIView.as_view(), name="deposit-list"),
    path(
        "<uuid:event_id>/deposits/new/",
        views.DepositCreateAPIView.as_view(),
        name="create-deposit",
    ),
    path(
        "<uuid:event_id>/deposits/<uuid:pk>/",
        views.DepositRUDAPIView.as_view(),
        name="rud-deposit",
    ),
    path(
        "<uuid:event_id>/repayments/", views.RepaymentListAPIView.as_view(), name="repayment-list"
    ),
    path(
        "<uuid:event_id>/repayments/new/",
        views.RepaymentCreateAPIView.as_view(),
        name="create-repayment",
    ),
    path(
        "<uuid:event_id>/repayments/<uuid:pk>/",
        views.RepaymentRUDAPIView.as_view(),
        name="rud-repayment",
    ),
]

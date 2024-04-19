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
        "<uuid:event_id>/transactions/",
        views.TransactionListAPIView.as_view(),
        name="transaction-list",
    ),
    path(
        "<uuid:event_id>/transactions/new/",
        views.TransactionCreateAPIView.as_view(),
        name="create-transaction",
    ),
    path(
        "<uuid:event_id>/transactions/<uuid:pk>/",
        views.TransactionRUDAPIView.as_view(),
        name="rud-transaction",
    ),
    path(
        "<uuid:event_id>/detailed-transaction/<uuid:pk>/",
        views.DetailedTransactionRUDAPIView.as_view(),
        name="rud-detailed-transaction",
    ),
    path(
        "<uuid:event_id>/transactions/<uuid:transaction_id>/movements/",
        views.MovementListAPIView.as_view(),
        name="movement-list",
    ),
    path(
        "<uuid:event_id>/transactions/<uuid:transaction_id>/movements/new/",
        views.MovementCreateAPIView.as_view(),
        name="create-movement",
    ),
    path(
        "<uuid:event_id>/transactions/<uuid:transaction_id>/movements/<uuid:pk>/",
        views.MovementRUDAPIView.as_view(),
        name="rud-movement",
    ),
]

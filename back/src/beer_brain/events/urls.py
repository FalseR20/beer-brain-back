from django.urls import path

from . import views

urlpatterns = [
    path("", views.EventListAPIView.as_view()),
    path("new/", views.EventCreateAPIView.as_view()),
    path("<uuid:pk>/", views.EventRetrieveUpdateAPIView.as_view()),
    path("<uuid:pk>/join/", views.join_event_api_view),
    path("<uuid:pk>/leave/", views.leave_event_api_view),
    path("<uuid:pk>/detailed/", views.FullEventRetrieveUpdateAPIView.as_view()),
    path("<uuid:event_id>/deposits/", views.DepositListAPIView.as_view()),
    path("<uuid:event_id>/deposits/new/", views.DepositCreateAPIView.as_view()),
    path("<uuid:event_id>/deposits/<uuid:pk>/", views.DepositRUDAPIView.as_view()),
    path("<uuid:event_id>/repayments/", views.RepaymentListAPIView.as_view()),
    path("<uuid:event_id>/repayments/new/", views.RepaymentCreateAPIView.as_view()),
    path("<uuid:event_id>/repayments/<uuid:pk>/", views.RepaymentRUDAPIView.as_view()),
]

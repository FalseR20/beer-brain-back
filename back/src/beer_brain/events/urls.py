from django.urls import path

from . import views

urlpatterns = [
    path("", views.EventListAPIView.as_view()),
    path("new/", views.EventCreateAPIView.as_view()),
    path("<str:pk>/", views.EventRetrieveUpdateAPIView.as_view()),
    path("<str:pk>/join/", views.join_event_api_view),
    path("<str:pk>/leave/", views.leave_event_api_view),
    path("<str:pk>/detailed/", views.FullEventRetrieveUpdateAPIView.as_view()),
    path("<str:event_id>/deposits/new/", views.DepositCreateAPIView.as_view()),
    path("<str:event_id>/deposits/<str:pk>/", views.DepositRetrieveUpdateDestroyAPIView.as_view()),
    path("<str:event_id>/deposits/", views.DepositListAPIView.as_view()),
    path("<str:event_id>/repayments/new/", views.RepaymentCreateAPIView.as_view()),
    path("<str:event_id>/repayments/<str:pk>/", views.RepaymentRUDAPIView.as_view()),
    path("<str:event_id>/repayments/", views.RepaymentListAPIView.as_view()),
]

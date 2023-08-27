from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from . import views

router = routers.DefaultRouter()
router.register("register", views.RegistrationViewSet, basename="register")

urlpatterns = [
    path("", include(router.urls)),
    path("token/", obtain_auth_token, name="api_token_auth"),
]

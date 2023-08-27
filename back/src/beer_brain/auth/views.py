from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .serializers import CreateUserSerializer


class RegistrationViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CreateUserSerializer

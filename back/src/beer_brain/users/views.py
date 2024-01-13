from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from . import serializers

User = get_user_model()


class UserCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = serializers.CreateUserSerializer


class SelfUserAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user


class UserGetAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_object(self):
        username = self.kwargs["username"]
        return get_object_or_404(self.get_queryset(), username=username)

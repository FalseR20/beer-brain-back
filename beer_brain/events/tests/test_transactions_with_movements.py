from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from beer_brain.events import models
from beer_brain.events.tests.test_events import User


class TransactionsWithMovementsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="test_password")
        self.host_user = User.objects.create_user(username="host_user", password="host_password")
        self.event = models.Event.objects.create(
            name="Event Name",
            description="Event Description",
            date="2024-01-01",
            host=self.host_user,
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_create_deposit(self):
        url = reverse("create-transaction", kwargs={"event_id": self.event.id})
        data = {
            "description": "test_transaction",
            "movements": [
                {
                    "username": self.host_user.username,
                    "delta": 50.0,
                    "cancel": False,
                },
            ],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data["description"], "test_transaction")
        movement = response.data["movements"][0]
        self.assertEqual(movement["user"]["username"], self.host_user.username)
        self.assertEqual(movement["delta"], "50.00")
        self.assertEqual(movement["cancel"], False)

    def test_create_movement_user_twice(self):
        url = reverse("create-transaction", kwargs={"event_id": self.event.id})
        data = {
            "description": "test_transaction",
            "movements": [
                {
                    "username": self.host_user.username,
                    "delta": 50.0,
                    "cancel": False,
                },
                {
                    "username": self.host_user.username,
                    "delta": 60.0,
                    "cancel": False,
                },
            ],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

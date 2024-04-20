from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from beer_brain.events import models
from beer_brain.events.tests.test_events import User


class TransactionsTests(TestCase):
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

    def create_transaction(self):
        url = reverse("create-transaction", kwargs={"event_id": self.event.id})
        data = {"description": "test transaction"}
        response = self.client.post(url, data)
        return response

    def test_create_transaction(self):
        response = self.create_transaction()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_transaction_list(self):
        url = reverse("transaction-list", kwargs={"event_id": self.event.id})
        self.create_transaction()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.create_transaction()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_transaction_detail(self):
        transaction = models.Transaction.objects.create(
            event=self.event,
            description="test_transaction",
        )
        url = reverse("rud-transaction", kwargs={"event_id": self.event.id, "pk": transaction.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], "test_transaction")

    def test_update_transaction(self):
        transaction = models.Transaction.objects.create(
            event=self.event,
            description="Original Description",
        )
        url = reverse("rud-transaction", kwargs={"event_id": self.event.id, "pk": transaction.id})
        data = {"description": "Updated Description"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        host_token = Token.objects.create(user=self.host_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {host_token}")
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transaction.refresh_from_db()
        self.assertEqual(transaction.description, "Updated Description")

    def test_delete_transaction(self):
        transaction = models.Transaction.objects.create(
            event=self.event,
            description="transaction Description",
        )
        url = reverse("rud-transaction", kwargs={"event_id": self.event.id, "pk": transaction.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        host_token = Token.objects.create(user=self.host_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {host_token}")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Transaction.objects.filter(id=transaction.id).exists())


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


class DetailedTransactionsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="test_password")
        self.host_user = User.objects.create_user(username="host_user", password="host_password")
        self.event = models.Event.objects.create(
            name="Event Name",
            description="Event Description",
            date="2024-01-01",
            host=self.host_user,
        )
        self.transaction = models.Transaction.objects.create(
            event=self.event,
            description="test_transaction",
        )
        self.movement = models.Movement.objects.create(
            transaction=self.transaction,
            user=self.user,
            delta=60.0,
            cancel=True,
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_get(self):
        url = reverse(
            "rud-detailed-transaction",
            kwargs={"event_id": self.event.id, "pk": self.transaction.id},
        )
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], "test_transaction")
        self.assertEqual(response.data["movements"][0]["delta"], "60.00")
        self.assertEqual(response.data["movements"][0]["cancel"], True)
        event = response.data["event"]
        self.assertEqual(event["name"], "Event Name")
        self.assertEqual(event["description"], "Event Description")
        self.assertEqual(event["host"]["username"], "host_user")

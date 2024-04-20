from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from beer_brain.events import models
from beer_brain.events.tests.test_events import User


class MovementTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="test_password")
        self.host_user = User.objects.create_user(username="host_user", password="host_password")
        self.event = models.Event.objects.create(
            name="Event Name",
            description="Event Description",
            date="2024-01-01",
            host=self.host_user,
        )
        self.event.users.set([self.host_user, self.user])
        self.transaction = models.Transaction.objects.create(
            event=self.event,
            description="Transaction description",
        )
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def create_movement(self, user: User):
        url = reverse(
            "create-movement",
            kwargs={"event_id": self.event.id, "transaction_id": self.transaction.id},
        )
        data = {"username": user.username, "value": 50.0, "cancel": False}
        response = self.client.post(url, data)
        return response

    def test_create_movement(self):
        response = self.create_movement(self.host_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_movement_list(self):
        url = reverse(
            "movement-list",
            kwargs={"event_id": self.event.id, "transaction_id": self.transaction.id},
        )
        self.create_movement(self.host_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.create_movement(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_movement_detail(self):
        movement = models.Movement.objects.create(
            user=self.user,
            transaction=self.transaction,
            delta=50.00,
            cancel=True,
        )
        url = reverse(
            "rud-movement",
            kwargs={
                "event_id": self.event.id,
                "transaction_id": self.transaction.id,
                "pk": movement.id,
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["username"], "test_user")
        self.assertEqual(response.data["delta"], "50.00")
        self.assertEqual(response.data["cancel"], True)

    def test_update_movement(self):
        movement = models.Movement.objects.create(
            user=self.user,
            transaction=self.transaction,
            delta=50.00,
            cancel=True,
        )
        url = reverse(
            "rud-movement",
            kwargs={
                "event_id": self.event.id,
                "transaction_id": self.transaction.id,
                "pk": movement.id,
            },
        )
        data = {"delta": 75.00}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        movement.refresh_from_db()
        self.assertEqual(movement.delta, 75.00)

    def test_delete_movement(self):
        movement = models.Movement.objects.create(
            user=self.user,
            transaction=self.transaction,
            delta=50.00,
            cancel=True,
        )
        url = reverse(
            "rud-movement",
            kwargs={
                "event_id": self.event.id,
                "transaction_id": self.transaction.id,
                "pk": movement.id,
            },
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Movement.objects.filter(id=movement.id).exists())

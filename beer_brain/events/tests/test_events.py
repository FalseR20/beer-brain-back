from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .. import models

User = get_user_model()


class EventTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="test_password")
        self.user2 = User.objects.create_user(username="second_user", password="second_password")
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def create_event(self):
        url = reverse("create-event")
        data = {
            "name": "Event Name",
            "description": "Event Description",
            "date": "2024-01-01",
        }
        response = self.client.post(url, data)
        return response

    def test_create_event(self):
        response = self.create_event()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Event Name")
        self.assertEqual(response.data["description"], "Event Description")
        self.assertEqual(response.data["date"], "2024-01-01")
        self.assertEqual(response.data["is_closed"], False)
        self.assertEqual(response.data["host"]["username"], self.user.username)
        self.assertEqual(len(response.data["users"]), 1)
        self.assertEqual(response.data["users"][0]["username"], self.user.username)

    def test_get_event_list(self):
        url = reverse("event-list")
        self.create_event()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.create_event()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_update_event(self):
        event = models.Event.objects.create(
            name="Original Name",
            description="Original Description",
            date="2024-01-01",
            host=self.user,
        )
        event.users.add(self.user)
        url = reverse("rud-event", kwargs={"pk": event.id})
        data = {"name": "Updated Name", "description": "Updated Description", "date": "2025-01-01"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        event.refresh_from_db()
        self.assertEqual(event.name, "Updated Name")
        self.assertEqual(event.description, "Updated Description")
        self.assertEqual(str(event.date), "2025-01-01")

    def test_transfer_host(self):
        event = models.Event.objects.create(
            name="Original Name",
            description="Original Description",
            date="2024-01-01",
            host=self.user,
        )
        event.users.add(self.user)
        event.users.add(self.user2)
        url = reverse("change-host", kwargs={"pk": event.id})
        data = {"new_host": "unknown_user"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {"new_host": "second_user"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        event.refresh_from_db()
        self.assertEqual(event.host, self.user2)
        # One more time without rights
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_event(self):
        event = models.Event.objects.create(
            name="Event Name",
            description="Event Description",
            date="2024-01-01",
            host=self.user,
        )
        event.users.add(self.user)
        url = reverse("rud-event", kwargs={"pk": event.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Event.objects.filter(id=event.id).exists())

    def test_join_event(self):
        event = models.Event.objects.create(
            name="Event Name",
            description="Event Description",
            date="2024-01-01",
            host=self.user2,
        )
        event.users.add(self.user2)
        url = reverse("join-event", kwargs={"pk": event.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(event.users.filter(id=self.user.id).exists())

    def test_leave_event(self):
        event = models.Event.objects.create(
            name="Event Name",
            description="Event Description",
            date="2024-01-01",
            host=self.user2,
        )
        event.users.set([self.user2, self.user])
        url = reverse("leave-event", kwargs={"pk": event.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(event.users.filter(id=self.user.id).exists())

    def test_leave_event_host(self):
        event = models.Event.objects.create(
            name="Event Name",
            description="Event Description",
            date="2024-01-01",
            host=self.user,
        )
        event.users.add(self.user)
        url = reverse("leave-event", kwargs={"pk": event.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

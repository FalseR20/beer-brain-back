from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from . import models

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
        self.assertEqual(len(response.data), 1)
        self.create_event()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

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


class DepositTests(TestCase):
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

    def create_deposit(self, value=100.00):
        url = reverse("create-deposit", kwargs={"event_id": self.event.id})
        data = {"value": value, "description": "Deposit Description"}
        response = self.client.post(url, data)
        return response

    def test_create_deposit(self):
        response = self.create_deposit()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_deposit_list(self):
        url = reverse("deposit-list", kwargs={"event_id": self.event.id})
        self.create_deposit()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.create_deposit()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_deposit_detail(self):
        deposit = models.Deposit.objects.create(
            user=self.user,
            event=self.event,
            value=100.00,
            description="Deposit Description",
        )
        url = reverse("rud-deposit", kwargs={"event_id": self.event.id, "pk": deposit.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["username"], "test_user")
        self.assertEqual(response.data["value"], "100.00")

    def test_update_deposit(self):
        deposit = models.Deposit.objects.create(
            user=self.user,
            event=self.event,
            value=100.00,
            description="Original Description",
        )
        url = reverse("rud-deposit", kwargs={"event_id": self.event.id, "pk": deposit.id})
        data = {"value": 150.00, "description": "Updated Description"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        deposit.refresh_from_db()
        self.assertEqual(deposit.value, 150.00)
        self.assertEqual(deposit.description, "Updated Description")

    def test_delete_deposit(self):
        deposit = models.Deposit.objects.create(
            user=self.user,
            event=self.event,
            value=100.00,
            description="Deposit Description",
        )
        url = reverse("rud-deposit", kwargs={"event_id": self.event.id, "pk": deposit.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Deposit.objects.filter(id=deposit.id).exists())


class RepaymentTests(TestCase):
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
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def create_repayment(self):
        url = reverse("create-repayment", kwargs={"event_id": self.event.id})
        data = {"recipient_username": self.host_user.username, "value": 50.0}
        response = self.client.post(url, data)
        return response

    def test_create_repayment(self):
        response = self.create_repayment()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_repayment_list(self):
        url = reverse("repayment-list", kwargs={"event_id": self.event.id})
        self.create_repayment()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.create_repayment()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_repayment_detail(self):
        repayment = models.Repayment.objects.create(
            payer=self.user,
            recipient=self.host_user,
            event=self.event,
            value=50.00,
            description="Test repayment",
        )
        url = reverse("rud-repayment", kwargs={"event_id": self.event.id, "pk": repayment.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["payer"]["username"], "test_user")
        self.assertEqual(response.data["recipient"]["username"], "host_user")
        self.assertEqual(response.data["value"], "50.00")
        self.assertEqual(response.data["description"], "Test repayment")

    def test_update_repayment(self):
        repayment = models.Repayment.objects.create(
            payer=self.user,
            recipient=self.host_user,
            event=self.event,
            value=50.00,
        )
        url = reverse("rud-repayment", kwargs={"event_id": self.event.id, "pk": repayment.id})
        data = {"value": 75.00}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        repayment.refresh_from_db()
        self.assertEqual(repayment.value, 75.00)

    def test_delete_repayment(self):
        repayment = models.Repayment.objects.create(
            payer=self.user,
            recipient=self.host_user,
            event=self.event,
            value=50.00,
        )
        url = reverse("rud-repayment", kwargs={"event_id": self.event.id, "pk": repayment.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Repayment.objects.filter(id=repayment.id).exists())


class DetailedEventTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="test_password")
        self.host_user = User.objects.create_user(username="host_user", password="host_password")
        self.event = models.Event.objects.create(
            name="Event Name",
            description="Event Description",
            date="2024-01-01",
            host=self.host_user,
        )
        self.event.users.set([self.user, self.host_user])
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def create_deposit(self, value=100.00):
        deposit_data = {
            "user": self.user,
            "event": self.event,
            "value": value,
            "description": "Deposit Description",
        }
        return models.Deposit.objects.create(**deposit_data)

    def create_repayment(self, value=50.00):
        repayment_data = {
            "payer": self.user,
            "recipient": self.host_user,
            "event": self.event,
            "value": value,
        }
        return models.Repayment.objects.create(**repayment_data)

    def test_get_detailed_event(self):
        self.create_deposit()
        self.create_repayment()
        url = reverse("get-detailed-event", kwargs={"pk": self.event.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        event_data = response.data
        self.assertEqual(event_data["name"], "Event Name")
        self.assertEqual(event_data["host"]["username"], "host_user")

        # Check deposits
        self.assertEqual(len(event_data["users"]), 2)
        user_data = event_data["users"][0]
        self.assertEqual(user_data["username"], "test_user")
        self.assertEqual(len(user_data["deposits"]), 1)
        deposit_data = user_data["deposits"][0]
        self.assertEqual(deposit_data["value"], "100.00")
        self.assertEqual(deposit_data["description"], "Deposit Description")

        # Check repayments
        self.assertEqual(len(user_data["repayments"]), 1)
        repayment_data = user_data["repayments"][0]
        self.assertEqual(repayment_data["value"], "50.00")

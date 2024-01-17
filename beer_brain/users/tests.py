from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()


class UserTests(TestCase):
    def setUp(self):
        self.user_username = "test_user"
        self.user_password = "test_password"
        self.user_data = {
            "username": self.user_username,
            "password": self.user_password,
        }
        self.user = User.objects.create_user(**self.user_data)
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()

    def test_user_creation(self):
        url = reverse("create-user")
        new_user_data = {
            "username": "new_user",
            "password": "new_password",
        }
        response = self.client.post(url, new_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_creation_invalid_data(self):
        url = reverse("create-user")
        data = {}  # Invalid data, missing required fields
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data_bad_username = {
            "username": "000",
            "password": "new_password",
        }
        response = self.client.post(url, data_bad_username)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data_short_username = {
            "username": "ab",
            "password": "new_password",
        }
        response = self.client.post(url, data_short_username)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        url = reverse("get-token")
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["token"], self.token.key)

    def test_user_login_invalid_credentials(self):
        url = reverse("get-token")
        invalid_data = {
            "username": self.user_username,
            "password": "invalid_password",
        }
        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_profile_me(self):
        url = reverse("get-my-user")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user_username)

    def test_get_user_profile_me_unauthorized(self):
        url = reverse("get-my-user")
        self.client.credentials()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_password(self):
        url = reverse("change-password")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        data = {
            "old_password": self.user_password,
            "new_password": "new_password",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify that the password has been changed
        self.assertTrue(
            User.objects.get(username=self.user_username).check_password("new_password")
        )

    def test_change_password_bad_old_one(self):
        url = reverse("change-password")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        data = {
            "old_password": "invalid_password",
            "new_password": "new_password",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_by_username(self):
        url = reverse("get-user", kwargs={"username": self.user_username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user_username)

    def test_get_user_by_username_unknown(self):
        url = reverse("get-user", kwargs={"username": "0_unknown"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

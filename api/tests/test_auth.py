from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase


class SingupTests(APITestCase):
    url = reverse("singup")

    def tearDown(self) -> None:
        User.objects.all().delete()

    def test_singup(self):
        username = "test_user"
        data = {"username": username, "password": "1234"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg="Check response status code. Should be equal to 201"
        )

        self.assertTrue(
            User.objects.filter(username=username).exists(),
            msg="Check if user is created in the DB successfully"
        )

    def test_duplicate_username(self):
        username = "duplicate_user"
        password = "1234"

        User.objects.create_user(username=username, password=password)

        data = {"username": username, "password": password}
        response = self.client.post(self.url, data, format="json")
        

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="Check response status code. Should be equal to 400, Since we are intentially testing the duplicate username case."
        )

        self.assertEqual(
            User.objects.filter(username=username).count(),
            1,
            msg="Check number of users exists in the DB with the defined username"
        )


class LoginTests(APITestCase):
    url = reverse("login")

    def setUp(self) -> None:
        User.objects.create_user(username="test_user", password="1234")
    
    def tearDown(self) -> None:
        User.objects.all().delete()
    
    def test_login(self):
        data = {"username": "test_user", "password": "1234"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg="Check response status code. Should be equal to 200, Since we are testing with valid credentials"
        )

    def test_invalid_username(self):
        data = {"username": "test_user1", "password": "1234"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg="Check response status code. Should be equal to 402, Since we are testing with invalid username"
        )
    
    def test_invalid_password(self):
        data = {"username": "test_user", "password": "12345"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg="Check response status code. Should be equal to 402, Since we are testing with invalid password"
        )

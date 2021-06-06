from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Employee, User
from api.utils import UserTypes


class EmployeeAuthTests(APITestCase):
    def setUp(self):
        self.credentials = {
            "username": "testemployee",
            "email": "employee@test.com",
            "password": "testpassword",
        }
        user = User(user_type=UserTypes.EMPLOYEE, **self.credentials)
        user.set_password(self.credentials["password"])
        user.save()
        Employee.objects.create(user=user)
        self.credentials.pop("email")

    def test_login(self):
        url = reverse("login")
        resp = self.client.post(url, data=self.credentials, follow=True)
        self.assertNotIn(b"errorlist", resp.content)
        self.assertTrue(resp.context["user"].is_authenticated)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.client.get(url)
        self.assertTrue(resp.context["user"].is_authenticated)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_logout(self):
        resp = self.client.post(
            reverse("login"),
            data=self.credentials,
            follow=True,
        )
        self.assertTrue(resp.context["user"].is_authenticated)

        resp = self.client.post(reverse("logout"), follow=True)

        self.assertFalse(resp.context["user"].is_authenticated)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Employee, User
from api.utils import UserTypes


class EmployeesAPITests(APITestCase):
    def setUp(self):
        self.employee_data = {
            "username": "testemployee",
            "email": "employee@test.com",
            "password": "testpassword",
            "first_name": "another",
            "last_name": "user",
        }
        self.user = User(user_type=UserTypes.EMPLOYEE, **self.employee_data)
        password = self.employee_data.pop("password")
        self.user.set_password(password)
        self.user.save()

        self.employee = Employee.objects.create(user=self.user, department="Tech")
        self.employee_data["pk"] = 1
        self.employee_data["department"] = "Tech"
        self.client.force_authenticate(self.user)

        self.admin_user = User(
            username="admin",
            email="admin@test.com",
            is_staff=True,
        )
        self.admin_user.set_password("adminpass")
        self.admin_user.save()

        self.new_employee_data = {
            "department": "Accounts",
            "user": {
                "username": "testemployee2",
                "email": "employee2@example.com",
                "first_name": "another",
                "last_name": "user",
                "password": "testpassword",
            },
        }

        self.employee_created_data = {
            "pk": 2,
            "department": "Accounts",
            "username": "testemployee2",
            "email": "employee2@example.com",
            "first_name": "another",
            "last_name": "user",
        }

        self.employee_patch_data = {
            "pk": 1,
            "department": "Tech",
            "user": {
                "username": "newemployee",
                "email": "new@test.com",
                "first_name": "another",
                "last_name": "user",
                "password": "testpassword",
            },
        }

    def test_get_employee_list(self, *args):

        # only admin can fetch all employee
        self.client.force_authenticate(self.admin_user)
        url = reverse("employee-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn(self.employee_data, resp.json()["results"])

    def test_create_employee(self):
        url = reverse("employee-list")
        resp = self.client.post(url, self.new_employee_data, format="json")
        print(resp.json())
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.employee_created_data, resp.json())

    def test_get_employee_detail(self):
        url = reverse(
            "employee-detail",
            kwargs={"pk": self.employee.pk},
        )
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(self.employee_data, resp.json())

    def test_update_employee(self):
        self.client.force_authenticate(self.user)
        url = reverse(
            "employee-detail",
            kwargs={"pk": self.employee.pk},
        )
        resp = self.client.patch(
            url,
            data=self.employee_patch_data,
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(self.employee_data, resp.json())

    def test_delete_employee(self):
        # only admin can delete employee data
        self.client.force_authenticate(self.admin_user)
        url = reverse(
            "employee-detail",
            kwargs={"pk": self.employee.pk},
        )
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Employee.objects.filter(pk=self.employee.pk).exists())

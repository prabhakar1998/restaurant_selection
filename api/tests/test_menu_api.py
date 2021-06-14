import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Employee, Menu, Restaurant, User
from api.utils import UserTypes


class RestaurantMenuAPITests(APITestCase):
    """Tests for List, Create menu for a restaurant.
    Tests GET, PATCH, DELETE of a menu for a restaurant"""

    def setUp(self):
        self.restaurant_data = {
            "username": "testrestaurant",
            "email": "restaurant@test.com",
            "password": "testpassword",
        }
        self.restaurant_user = User(
            user_type=UserTypes.RESTAURANT, **self.restaurant_data
        )
        password = self.restaurant_data.pop("password")
        self.restaurant_user.set_password(password)
        self.restaurant_user.save()

        self.admin_user = User(
            username="admin",
            email="admin@test.com",
            is_staff=True,
        )
        self.admin_user.set_password("adminpass")
        self.admin_user.save()

        self.restaurant = Restaurant.objects.create(
            user=self.restaurant_user,
            restaurant_name="restaurant1",
        )
        self.restaurant_data["restaurant_id"] = 1
        self.restaurant_data["restaurant_name"] = "restaurant1"
        date_posted = str(datetime.date.today())
        self.menu1 = Menu.objects.create(
            restaurant=self.restaurant,
            title="Dish 1",
            description="Dish 1 ingredients.",
        )
        self.menu2 = Menu.objects.create(
            restaurant=self.restaurant,
            title="Dish 2",
            description="Dish 2 ingredients.",
        )

        self.menu1_data = {
            "id": 1,
            "restaurant": 1,
            "title": "Dish 1",
            "description": "Dish 1 ingredients.",
            "date_posted": date_posted,
        }
        self.menu2_data = {
            "id": 2,
            "restaurant": 1,
            "title": "Dish 2",
            "description": "Dish 2 ingredients.",
            "date_posted": date_posted,
        }

        self.menu2_updated_data = {
            "id": 1,
            "restaurant": 1,
            "title": "Dish 3",
            "description": "Dish 3 ingredients.",
            "date_posted": date_posted,
        }

        self.menu_data = [self.menu1_data, self.menu2_data]
        self.employee_user = User(
            user_type=UserTypes.EMPLOYEE,
            username="employee1",
            email="employee@test.com",
        )
        self.employee_user.set_password("employeepass")
        self.employee_user.save()
        self.employee = Employee.objects.create(
            user=self.restaurant_user, department="Tech"
        )
        self.new_menu_data = {
            "restaurant": 1,
            "title": "Dish 3",
            "description": "Dish 3 ingredients.",
        }

    def test_get_menu_list(self, *args):
        # only employee or admin can fetch all menus for today
        self.client.force_authenticate(self.employee_user)
        url = reverse("menu-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        assert self.menu_data == resp.json()["results"]

    def test_create_menu(self):
        self.client.force_authenticate(self.restaurant_user)
        url = reverse("menu-list")
        resp = self.client.post(url, self.new_menu_data, format="json")
        date_posted = str(datetime.date.today())
        self.new_menu_data["id"] = 3
        self.new_menu_data["date_posted"] = date_posted
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.new_menu_data, resp.json())

    def test_get_menu_detail(self):
        self.client.force_authenticate(self.admin_user)
        url = reverse("menu-detail", kwargs={"pk": self.menu1.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(self.menu1_data, resp.json())

    def test_update_menu(self):
        self.client.force_authenticate(self.admin_user)
        url = reverse("menu-detail", kwargs={"pk": self.menu1.id})
        resp = self.client.patch(url, data=self.new_menu_data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(self.menu2_updated_data, resp.json())

    def test_delete_menu(self):
        # only admin can delete menu data
        self.client.force_authenticate(self.admin_user)
        url = reverse("menu-detail", kwargs={"pk": self.menu1.id})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Menu.objects.filter(pk=self.menu1.id).exists())

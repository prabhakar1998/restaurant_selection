from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Restaurant, User
from api.utils import UserTypes


class RestaurantsAPITests(APITestCase):
    def setUp(self):
        self.restaurant_data = {
            "username": "testrestaurant",
            "email": "restaurant@test.com",
            "password": "testpassword",
        }
        self.user = User(user_type=UserTypes.RESTAURANT, **self.restaurant_data)
        password = self.restaurant_data.pop("password")
        self.user.set_password(password)
        self.user.save()

        self.restaurant = Restaurant.objects.create(
            user=self.user, restaurant_name="restaurant1"
        )
        self.restaurant_data["pk"] = 1
        self.restaurant_data["restaurant_name"] = "restaurant1"
        self.client.force_authenticate(self.user)

        self.admin_user = User(
            username="admin",
            email="admin@test.com",
            is_staff=True,
        )
        self.admin_user.set_password("adminpass")
        self.admin_user.save()

        self.new_restaurant_data = {
            "restaurant_name": "restaurant2",
            "user": {
                "username": "testrestaurant2",
                "email": "restaurant2@example.com",
                "password": "testpassword",
            },
        }

        self.restaurant_created = {
            "pk": 2,
            "restaurant_name": "restaurant2",
            "username": "testrestaurant2",
            "email": "restaurant2@example.com",
        }

        self.restaurant_patch_data = {
            "pk": 1,
            "restaurant_name": "restaurant1",
            "user": {
                "username": "newrestaurant",
                "email": "new@test.com",
                "password": "testpassword",
            },
        }

    def test_get_restaurant_list(self, *args):
        # only admin can fetch all restaurant
        self.client.force_authenticate(self.admin_user)
        url = reverse("restaurant-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn(self.restaurant_data, resp.json()["results"])

    def test_create_restaurant(self):
        url = reverse("restaurant-list")
        resp = self.client.post(url, self.new_restaurant_data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.restaurant_created, resp.json())

    def test_get_restaurant_detail(self):
        url = reverse(
            "restaurant-detail",
            kwargs={"pk": self.restaurant.pk},
        )
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(self.restaurant_data, resp.json())

    def test_update_restaurant(self):
        self.client.force_authenticate(self.user)
        url = reverse(
            "restaurant-detail",
            kwargs={"pk": self.restaurant.pk},
        )
        resp = self.client.patch(
            url,
            data=self.restaurant_patch_data,
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(self.restaurant_data, resp.json())

    def test_delete_restaurant(self):
        # only admin can delete restaurant data
        self.client.force_authenticate(self.admin_user)
        url = reverse(
            "restaurant-detail",
            kwargs={"pk": self.restaurant.pk},
        )
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Restaurant.objects.filter(pk=self.restaurant.pk).exists())

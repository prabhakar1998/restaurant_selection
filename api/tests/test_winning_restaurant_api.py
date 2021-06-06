import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.constants import MAX_CONSECUTIVE_WINNINGS
from api.models import Employee, Menu, Restaurant, User, Vote
from api.utils import UserTypes


class WinningRestaurantTests(APITestCase):
    """Test for GET api for all the votes for today"""

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
        self.restaurant_data["restaurant_id"] = 1
        self.restaurant_data["restaurant_name"] = "restaurant1"
        date_posted = str(datetime.date.today())
        self.menu1 = Menu.objects.create(
            restaurant=self.restaurant,
            title="Dish 1",
            description="Dish 1 ingredients.",
        )

        menu1_data = {
            "id": 1,
            "restaurant_id": 1,
            "title": "Dish 1",
            "description": "Dish 1 ingredients.",
            "date_posted": date_posted,
            "restaurant_name": "restaurant1",
        }

        self.menu_data = [menu1_data]

        self.employee_user = User(
            user_type=UserTypes.EMPLOYEE,
            username="employee1",
            email="employee@test.com",
        )
        self.employee_user.set_password("employeepass")
        self.employee_user.save()
        self.employee = Employee.objects.create(
            user=self.employee_user, department="Tech"
        )

        self.employee2_user = User(
            user_type=UserTypes.EMPLOYEE,
            username="employee2",
            email="employee2@test.com",
        )
        self.employee2_user.set_password("employeepass")
        self.employee2_user.save()
        self.employee_2 = Employee.objects.create(
            user=self.employee2_user, department="Tech"
        )

        self.votes = Vote.objects.create(
            restaurant=self.restaurant, menu=self.menu1, employee=self.employee
        )
        date_voted = date_posted
        self.votes_data = [
            {
                "pk": 1,
                "restaurant": 1,
                "employee": 1,
                "date_voted": date_voted,
                "menu": 1,
            }
        ]
        self.new_vote_emp1 = {"restaurant": 1, "employee": 1, "menu": 1}
        self.fist_day_winner = {"restaurant_id": 1, "total_votes": 1}
        self.consecutive_error = [
            f"Restaurant {self.restaurant} is consecutive winner"
            f" for {MAX_CONSECUTIVE_WINNINGS} times and can not be voted."
        ]

    def test_get_winning_restaurant(self, *args):
        # only employee or admin can fetch all votes
        self.client.force_authenticate(self.employee_user)
        url = reverse("winning-restaurant-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        assert self.fist_day_winner == resp.json()["results"][0]

    def test_consecutive_winning_restaurant(self, *args):
        """If a restaurant is winning from past two working
        days then it can't be voted and it will not win."""
        Vote.objects.filter(employee=1).delete()
        for day in range(1, MAX_CONSECUTIVE_WINNINGS + 1):
            # making restaurant winner for MAX_CONSECUTIVE_WINNINGS timer in previous days
            date_voted = str((datetime.datetime.now() - datetime.timedelta(day)).date())
            Vote.objects.create(
                restaurant=self.restaurant,
                menu=self.menu1,
                employee=self.employee,
                date_voted=date_voted,
            )

        self.client.force_authenticate(self.employee_user)
        url = reverse("vote-list")
        resp = self.client.post(url, self.new_vote_emp1, format="json")
        self.assertEqual(self.consecutive_error, resp.json()["non_field_errors"])
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

import datetime

from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from api.constants import MAX_CONSECUTIVE_WINNINGS
from api.models import Employee, Menu, Restaurant, User, Vote
from api.utils import UserTypes


class EmployeeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
        )
        extra_kwargs = {"password": {"write_only": True}}

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=("email",),
                message="This email is already used by another user.",
            )
        ]


class EmployeeProfileSerializer(serializers.ModelSerializer):

    user = EmployeeUserSerializer(partial=True)

    class Meta:
        model = Employee
        fields = ("pk", "department", "user")

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        password = user_data.pop("password")
        user = User(user_type=UserTypes.EMPLOYEE, **user_data)
        if password:
            user.set_password(password)
            user.save()
            employee = Employee.objects.create(user=user, **validated_data)
            employee.save()
            return employee

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        instance.department = validated_data.pop("department", instance.department)
        instance.user.first_name = user_data.get("first_name", instance.user.first_name)
        instance.user.last_name = user_data.get("last_name", instance.user.last_name)
        password = user_data.get("password", "")
        if password:
            instance.user.set_password(password)
        instance.user.save()
        instance.save()
        return instance

    def to_representation(self, obj):
        """Move fields from Restaurant to User representation."""
        representation = super().to_representation(obj)
        user_representation = representation.pop("user")
        if user_representation:
            for key in user_representation:
                representation[key] = user_representation[key]
        return representation


class RestaurantUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=("email",),
                message="This email is already used by another user.",
            )
        ]


class RestaurantProfileSerializer(serializers.ModelSerializer):

    user = RestaurantUserSerializer(required=True)

    class Meta:
        model = Restaurant
        fields = ("pk", "restaurant_name", "user")

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        password = user_data.pop("password")
        if password:
            user = User(user_type=UserTypes.RESTAURANT, **user_data)
            user.set_password(password)
            user.save()
            instance = Restaurant.objects.create(user=user, **validated_data)
            return instance

    def update(self, instance, validated_data):
        instance.restaurant_name = validated_data.get(
            "restaurant_name", instance.restaurant_name
        )
        instance.save()
        return instance

    def to_representation(self, obj):
        """Move fields from Restaurant to User representation."""
        representation = super().to_representation(obj)
        user_representation = representation.pop("user")
        if user_representation:
            for key in user_representation:
                representation[key] = user_representation[key]
        return representation


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = (
            "id",
            "restaurant",
            "title",
            "description",
            "date_posted",
        )


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = (
            "pk",
            "restaurant",
            "employee",
            "date_voted",
            "menu",
            "pk",
        )

    def validate(self, validated_data):
        request = self.context["request"]
        restaurant = get_object_or_404(Restaurant, pk=request.data.get("restaurant"))
        menu = get_object_or_404(Menu, pk=request.data.get("menu"))
        employee = get_object_or_404(Employee, pk=request.data.get("employee"))
        if employee.user != request.user:
            raise PermissionDenied()
        previous_voted_dates = [
            each_row["date_voted"]
            for each_row in Vote.objects.values("date_voted").distinct()[
                : MAX_CONSECUTIVE_WINNINGS + 1
            ]
            if each_row["date_voted"] != datetime.date.today()
        ]
        if len(previous_voted_dates) > 1:
            previous_winner = set()
            for each_date in previous_voted_dates:
                restaurant_id = (
                    Vote.objects.filter(date_voted=each_date)
                    .values("restaurant_id")
                    .annotate(total_votes=Count("restaurant_id"))
                    .order_by("-total_votes")[:1][0]["restaurant_id"]
                )
                previous_winner.add(restaurant_id)
            if len(previous_winner) == 1:
                restricted_restaurant = previous_winner.pop()
                if restaurant.pk == restricted_restaurant:
                    raise serializers.ValidationError(
                        f"Restaurant {restaurant.restaurant_name} is consecutive winner"
                        f" for {MAX_CONSECUTIVE_WINNINGS} times and can not be voted."
                    )
        if menu.restaurant != restaurant:
            raise serializers.ValidationError(
                f"Restaurant {restaurant.restaurant_name} is not having menu voted"
            )
        if menu.date_posted != datetime.date.today():
            raise serializers.ValidationError(
                f"Only todays menu can be voted. Menu {menu} was posted on {menu.date_posted}"
            )
        else:
            votes = Vote.objects.filter(
                employee=employee,
                date_voted=datetime.date.today(),
            ).values("id")
            if votes.count() > 0:
                raise serializers.ValidationError("You have already voted for today.")
        return validated_data

    def create(self, validated_data):
        self.validate(validated_data)
        instance = Vote.objects.create(**validated_data)
        return instance


class TotalVoteSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return instance["total_votes"]


class WinnerSerializer(serializers.ModelSerializer):

    total_votes = TotalVoteSerializer(source="*")

    class Meta:
        model = Vote
        fields = (
            "pk",
            "restaurant_id",
            "employee_id",
            "pk",
            "total_votes",
        )

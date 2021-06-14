import datetime
import logging

from django.db.models import Count
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from api.filters import MenuFilter, VoteFilter
from api.models import Employee, Menu, Restaurant, Vote
from api.permissions import (EmployeeViewSetPermission, IsEmployeeUserOrAdmin,
                             MenuViewSetPermission,
                             RestaurantViewSetPermission)
from api.serializers import (EmployeeProfileSerializer, MenuSerializer,
                             RestaurantProfileSerializer, VoteSerializer,
                             WinnerSerializer)

logger = logging.getLogger(__name__)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeProfileSerializer
    permission_classes = [EmployeeViewSetPermission]

    def list(self, request, *args, **kwargs):
        logger.info(
            f"User {request.user} GET employee-list with args {dict(request.query_params)}"
        )
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(
            f"User {request.user} POST employee-list with args "
            f"{dict(request.query_params)} and data {request.data}"
        )
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, pk, *args, **kwargs):
        logger.info(
            f"User {request.user} GET employee-detail for employee {pk}"
            f" with args {dict(request.query_params)}"
        )
        return super().retrieve(request, pk, *args, **kwargs)

    def partial_update(self, request, pk, *args, **kwargs):
        logger.info(
            f"User {request.user} PATCH employee-detail for employee {pk} with args "
            f"{dict(request.query_params)} and data {request.data}"
        )
        return super().partial_update(request, pk, *args, **kwargs)

    def destroy(self, request, pk, *args, **kwargs):
        logger.info(f"User {request.user} DELETE employee-detail for employee {pk}")
        return super().destroy(request, pk, *args, **kwargs)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantProfileSerializer
    permission_classes = [RestaurantViewSetPermission]

    def list(self, request, *args, **kwargs):
        logger.info(
            f"User {request.user} GET restaurant-list with args {dict(request.query_params)}"
        )
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(
            f"User {request.user} POST restaurant-list with args "
            f"{dict(request.query_params)} and data {request.data}"
        )
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, pk, *args, **kwargs):
        logger.info(
            f"User {request.user} GET restaurant-detail for restaurant"
            f" {pk} with args {dict(request.query_params)}"
        )
        return super().retrieve(request, pk, *args, **kwargs)

    def partial_update(self, request, pk, *args, **kwargs):
        logger.info(
            f"User {request.user} PATCH restaurant-detail for restaurant {pk} with args "
            f"{dict(request.query_params)} and data {request.data}"
        )
        return super().partial_update(request, pk, *args, **kwargs)

    def destroy(self, request, pk, *args, **kwargs):
        logger.info(f"User {request.user} DELETE restaurant-detail for restaurant {pk}")
        return super().destroy(request, pk, *args, **kwargs)


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filterset_class = MenuFilter
    permission_classes = [MenuViewSetPermission]

    def list(self, request, *args, **kwargs):
        logger.info(
            f"User {request.user} GET menu-list with args {dict(request.query_params)}"
        )
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(
            f"User {request.user} POST menu-list with args "
            f"{dict(request.query_params)} and data {request.data}"
        )
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, pk, *args, **kwargs):
        logger.info(
            f"User {request.user} GET menu-detail for menu {pk} "
            "with args {dict(request.query_params)}"
        )
        return super().retrieve(request, pk, *args, **kwargs)

    def partial_update(self, request, pk, *args, **kwargs):
        logger.info(
            f"User {request.user} PATCH menu-detail for menu {pk} "
            f"with args {dict(request.query_params)} and data {request.data}"
        )
        return super().partial_update(request, pk, *args, **kwargs)

    def destroy(self, request, pk, *args, **kwargs):
        logger.info(f"User {request.user} DELETE menu-detail for menu {pk}")
        return super().destroy(request, pk, *args, **kwargs)


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    filterset_class = VoteFilter
    serializer_class = VoteSerializer
    permission_classes = [IsEmployeeUserOrAdmin]

    def list(self, request, *args, **kwargs):
        logger.info(
            f"User {request.user} GET vote-list with args {dict(request.query_params)}"
        )
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(
            f"User {request.user} POST vote-list with args "
            f"{dict(request.query_params)} and data {request.data}"
        )
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, pk, *args, **kwargs):
        logger.info(
            f"User {request.user} GET vote-detail for vote"
            f" {pk} with args {dict(request.query_params)}"
        )
        return super().retrieve(request, pk, *args, **kwargs)


class WinnerViewSet(viewsets.ModelViewSet):
    queryset = (
        Vote.objects.filter(date_voted=datetime.date.today())
        .values("restaurant_id")
        .annotate(total_votes=Count("restaurant_id"))
        .order_by("-total_votes")[:1]
    )

    serializer_class = WinnerSerializer
    permission_classes = [IsEmployeeUserOrAdmin]

    def list(self, request, *args, **kwargs):
        logger.info(
            f"User {request.user} GET winning-restaurant-list "
            f"with args {dict(request.query_params)}"
        )
        return super().list(request, *args, **kwargs)

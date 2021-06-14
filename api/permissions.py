from django.urls import reverse
from rest_framework import permissions

from api.utils import UserTypes


class IsEmployeeUserOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.user_type == UserTypes.EMPLOYEE or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.path == reverse("vote-detail", kwargs={"pk": obj.pk}):
            return obj.employee.user == request.user or request.user.is_staff
        return request.user.is_staff or request.user.user_type == UserTypes.EMPLOYEE


class EmployeeViewSetPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            if view.action == "create":
                return True
            else:
                return False
        if view.action == "create":
            return True
        elif (
            view.action == "retrieve"
            or view.action == "update"
            or view.action == "partial_update"
        ):
            return request.user.user_type == UserTypes.EMPLOYEE or request.user.is_staff
        elif view.action == "list" or view.action == "destroy":
            return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.path == reverse("employee-detail", kwargs={"pk": obj.pk}):
            return obj.user == request.user or request.user.is_staff
        return request.user.is_staff or request.user.user_type == UserTypes.EMPLOYEE


class RestaurantViewSetPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            if view.action == "create":
                return True
            else:
                return False
        if view.action == "create":
            return True
        elif (
            view.action == "destroy"
            or view.action == "update"
            or view.action == "partial_update"
        ):
            return (
                request.user.user_type == UserTypes.RESTAURANT or request.user.is_staff
            )
        elif view.action == "retrieve" or view.action == "list":
            return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.path == reverse("restaurant-detail", kwargs={"pk": obj.pk}):
            return obj.user == request.user or request.user.is_staff
        return request.user.is_staff or request.user.user_type == UserTypes.RESTAURANT


class MenuViewSetPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if view.action == "create":
            return (
                request.user.user_type == UserTypes.RESTAURANT or request.user.is_staff
            )
        elif view.action == "list":
            return request.user.user_type == UserTypes.EMPLOYEE or request.user.is_staff
        elif (
            view.action == "destroy"
            or view.action == "update"
            or view.action == "partial_update"
        ):
            return request.user and request.user.is_staff
        elif view.action == "retrieve":
            return request.user.is_authenticated

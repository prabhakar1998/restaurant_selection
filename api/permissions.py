from django.urls import reverse
from rest_framework import permissions

from api.utils import UserTypes


class IsLoggedInUserOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff


class IsRestarauntUserOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.user_type == UserTypes.RESTAURANT or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.path == reverse("restaurant-detail", kwargs={"pk": obj.pk}):
            return obj.user == request.user or request.user.is_staff
        return request.user.is_staff or request.user.user_type == UserTypes.RESTAURANT


class IsEmployeeUserOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.user_type == UserTypes.EMPLOYEE or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.path == reverse("vote-detail", kwargs={"pk": obj.pk}):
            return obj.employee.user == request.user or request.user.is_staff
        return request.user.is_staff or request.user.user_type == UserTypes.EMPLOYEE

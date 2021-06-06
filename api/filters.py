import datetime

from django.urls import reverse
from django_filters import rest_framework as filters

from api.models import Menu, Vote


class MenuFilter(filters.FilterSet):

    include_previous = filters.BooleanFilter(
        method="include_previous_filter",
        help_text='Older menus are excluded by default, use "true" to include them.',
    )

    class Meta:
        model = Menu
        fields = ["restaurant", "date_posted"]

    def __init__(self, data=None, *args, **kwargs):
        is_list_url = kwargs.get("id") is None and kwargs.get(
            "request"
        ).path == reverse("menu-list")
        if is_list_url and data is not None and "include_previous" not in data:
            data = data.copy()
            data["include_previous"] = "false"
        super().__init__(data, *args, **kwargs)

    def include_previous_filter(self, queryset, name, value):
        if value is False:
            queryset = queryset.filter(date_posted=datetime.date.today())
        return queryset


class VoteFilter(filters.FilterSet):

    include_previous = filters.BooleanFilter(
        method="include_previous_filter",
        help_text='Older votes are excluded by default, use "true" to include them.',
    )

    class Meta:
        model = Vote
        fields = [
            "restaurant",
            "date_voted",
            "employee",
            "menu",
        ]

    def __init__(self, data=None, *args, **kwargs):
        is_list_url = kwargs.get("id") is None and kwargs.get(
            "request"
        ).path == reverse("vote-list")
        if is_list_url and data is not None and "include_previous" not in data:
            data = data.copy()
            data["include_previous"] = "false"
        super().__init__(data, *args, **kwargs)

    def include_previous_filter(self, queryset, name, value):
        if value is False:
            queryset = queryset.filter(date_voted=datetime.date.today())
        return queryset

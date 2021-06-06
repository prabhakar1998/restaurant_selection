from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from api.views import (EmployeeViewSet, MenuViewSet, RestaurantViewSet,
                       VoteViewSet, WinnerViewSet)

urlpatterns = [
    path(
        "employee/",
        EmployeeViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="employee-list",
    ),
    path(
        "employee/<int:pk>/",
        EmployeeViewSet.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="employee-detail",
    ),
    path(
        "restaurant/",
        RestaurantViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="restaurant-list",
    ),
    path(
        "restaurant/<int:pk>/",
        RestaurantViewSet.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="restaurant-detail",
    ),
    path(
        "menu/",
        MenuViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="menu-list",
    ),
    path(
        "menu/<int:pk>",
        MenuViewSet.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="menu-detail",
    ),
    path(
        "winning_restaurant/",
        WinnerViewSet.as_view(
            {
                "get": "list",
            }
        ),
        name="winning-restaurant-list",
    ),
    path(
        "vote/",
        VoteViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="vote-list",
    ),
    path(
        "vote/<int:pk>",
        VoteViewSet.as_view(
            {
                "get": "retrieve",
            }
        ),
        name="vote-detail",
    ),
    path(
        "token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "token/verify/",
        TokenVerifyView.as_view(),
        name="token_verify",
    ),
]

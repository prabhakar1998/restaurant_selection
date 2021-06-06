from django.conf.urls import include
from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Restaurant selection API",
        default_version="v1",
        description="This API allows to manage employees, restaurants and vote for restaurants.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    re_path(r"^api/", include("api.urls")),
    re_path("accounts/", include("django.contrib.auth.urls")),
    re_path(
        r"",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger-ui",
    ),
]

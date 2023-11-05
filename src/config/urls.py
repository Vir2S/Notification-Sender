from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from .api import ping


API_ROOT = "api/v1"

schema_view = get_schema_view(
    openapi.Info(
        title="Notification Sender API",
        default_version="v1",
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Ping - Pong :-)
    path("", ping, name="ping"),

    path(
        f"{API_ROOT}/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(f"{API_ROOT}/auth/", include("authentication.urls")),
    path(f"{API_ROOT}/users/", include("users.urls")),
    path(f"{API_ROOT}/notifications/", include("notifications.urls"))
]

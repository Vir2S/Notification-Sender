from django.contrib import admin
from django.urls import path, include


API_ROOT = "api/v1"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{API_ROOT}/auth/", include("authentication.urls")),
    path(f"{API_ROOT}/users/", include("users.urls")),
]

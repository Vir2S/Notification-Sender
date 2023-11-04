from django.urls import path
from drf_yasg.utils import swagger_auto_schema

from users.api import UserListCreateAPIView
from users.serializers import UserPublicSerializer


urlpatterns = [
    path(
        "",
        swagger_auto_schema(
            methods=["get", "post"],
            responses={200: UserPublicSerializer, 201: UserPublicSerializer}
        )(
            UserListCreateAPIView.as_view()
        ),
    ),
]

from django.urls import path
from drf_yasg.utils import swagger_auto_schema

from users.api import UserListCreateAPIView
from users.serializers import UserPublicSerializer


urlpatterns = [
    path("", UserListCreateAPIView.as_view()),
]

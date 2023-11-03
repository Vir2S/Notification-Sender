from django.urls import path

from users.api import UserCreateAPIView


urlpatterns = [
    path("", UserCreateAPIView.as_view()),
]

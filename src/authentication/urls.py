from django.urls import path
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.api import UserSignUpCreateAPIView
from authentication.serializers import LoginResponseSerializer


urlpatterns = [
    path(
        "signin/",
        swagger_auto_schema(
            method="post",
            responses={201: LoginResponseSerializer}
        )(
            TokenObtainPairView.as_view()
        ),
    ),
    path("signup/", UserSignUpCreateAPIView.as_view())
]

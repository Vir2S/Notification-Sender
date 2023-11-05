from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from users.constants import Role
from users.serializers import UserCreateSerializer, UserPublicSerializer


User = get_user_model()


class UserListCreateAPIView(ListCreateAPIView):
    serializer_class = UserCreateSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return User.objects.none()

        if user.role == Role.ADMIN:
            return User.objects.all()

        return User.objects.filter(id=user.id)

    @swagger_auto_schema(responses={200: UserPublicSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserPublicSerializer(queryset, many=True)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )

    @swagger_auto_schema(responses={201: UserPublicSerializer()})
    def post(self, request):
        create_serializer = self.get_serializer(data=request.data)
        create_serializer.is_valid(raise_exception=True)
        self.perform_create(create_serializer)

        public_serializer = UserPublicSerializer(create_serializer.instance)
        headers = self.get_success_headers(public_serializer.data)

        return Response(
            public_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

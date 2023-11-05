from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from users.permissions import IsAdminOrUnregistered
from users.serializers import UserCreateSerializer, UserPublicSerializer


class UserSignUpCreateAPIView(CreateAPIView):
    permission_classes = [IsAdminOrUnregistered]
    serializer_class = UserCreateSerializer

    @swagger_auto_schema(responses={201: UserPublicSerializer()})
    def post(self, request, *args, **kwargs):
        create_serializer = self.get_serializer(data=request.data)

        if create_serializer.is_valid():
            self.perform_create(create_serializer)
            public_serializer = UserPublicSerializer(create_serializer.instance)
            headers = self.get_success_headers(public_serializer.data)

            return Response(
                public_serializer.data, status=201, headers=headers
            )

        return Response(create_serializer.errors, status=400)

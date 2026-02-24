from rest_framework import generics, permissions

from apps.authentication.api.v1.serializers import RegisterSerializer
from apps.authentication.models import UserModel
from apps.authentication.services import UserService


class RegisterView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    permission_classes = [permissions.AllowAny]  # qualquer pessoa pode se registrar
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user_instance = serializer.save()
        UserService().register_user(user_instance)

from rest_framework import generics, permissions

from apps.authentication.models import UserModel
from apps.authentication.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    permission_classes = [permissions.AllowAny]  # qualquer pessoa pode se registrar
    serializer_class = RegisterSerializer

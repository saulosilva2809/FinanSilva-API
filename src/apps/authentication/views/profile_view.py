from rest_framework import generics, permissions

from apps.authentication.serializers import UpdateProfileSerializer, ViewProfileSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return UpdateProfileSerializer

        elif self.request.method in ['GET']:
            return ViewProfileSerializer

    def get_object(self):
        return self.request.user

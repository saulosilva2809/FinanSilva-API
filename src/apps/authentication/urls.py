from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    LogoutView,
    ProfileView,
    RegisterView,
)


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),

    # profile
    path('profile/', ProfileView.as_view(), name='profile'),
]

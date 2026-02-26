from django.urls import path


from .docs import schemas
from .views import (
    LogoutView,
    ProfileView,
    RegisterView,
)


urlpatterns = [
    path('login/', schemas.CustomTokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('refresh/', schemas.CustomTokenRefreshView.as_view(), name='refresh'),

    # profile
    path('profile/', ProfileView.as_view(), name='profile'),
]

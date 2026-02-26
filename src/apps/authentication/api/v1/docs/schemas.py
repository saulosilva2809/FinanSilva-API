from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.authentication.api.v1.docs.serializers import (
    ProfileResponseSerializer,
    RegisterRequestResponseSerializer,
    UpdateProfileRequestSerializer,
)
from apps.authentication.api.v1.views import (
    RegisterView,
    ProfileView,
    LogoutView,
)


RegisterView = extend_schema_view(
    post=extend_schema(
        tags=['Authentication'],
        summary='Registrar novo usuário',
        description='Cria novo usuário com base nos dados fornecidos',
        request=RegisterRequestResponseSerializer,
        responses={200: RegisterRequestResponseSerializer}
    )
)(RegisterView)


CustomTokenObtainPairView = extend_schema_view(
    post=extend_schema(
        tags=['Authentication'],
        summary='Realizar login',
        description='Gera um par de tokens (access e refresh) para um usuário autenticado.',
    )
)(TokenObtainPairView)


CustomTokenRefreshView = extend_schema_view(
    post=extend_schema(
        tags=['Authentication'],
        summary='Renovar token de acesso',
        description='Utiliza o refresh token para gerar um novo access token.',
    )
)(TokenRefreshView)


ProfileView = extend_schema_view(
    get=extend_schema(
        tags=['Authentication'],
        summary='Visualizar o perfil do usuário',
        description='Permite a visualização do perfil do usuário.',
        responses={200: ProfileResponseSerializer}
    ),
    put=extend_schema(
        tags=['Authentication'],
        summary='Atualizar informações do usuário',
        description='Permite atualizar o perfil do usuário.',
        request=UpdateProfileRequestSerializer,
        responses={200: ProfileResponseSerializer}
    ),
    patch=extend_schema(
        tags=['Authentication'],
        summary='Atualizar informações do usuário',
        description='Permite atualizar o perfil do usuário.',
        request=UpdateProfileRequestSerializer,
        responses={200: ProfileResponseSerializer}
    )
)(ProfileView)


LogoutView = extend_schema_view(
    post=extend_schema(
        tags=['Authentication'],
        summary='Realizar logout do usuário',
        description='Permite o usuário sair da conta e fazer logout.',
        responses={205: None}
    )
)(LogoutView)

from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.account.api.v1.docs.serializers import (
    AccountResponseSerializer,
    CreateAccountRequestSerializer,
    CreateAccountResponseSerializer,
    UpdateAccountRequestSerializer,
)
from apps.account.api.v1.views import (
    AccountListCreateView,
    AccountRetrieveUpdateDestroyView,
)


AccountListCreateView = extend_schema_view(
    get=extend_schema(
        tags=['Accounts'],
        summary='Listar contas',
        description='Retorna todas as contas do usuário.',
        responses=AccountResponseSerializer,
    ),

    post=extend_schema(
        tags=['Accounts'],
        summary='Criar conta',
        description='Cria uma nova conta financeira para o usuário.',
        request=CreateAccountRequestSerializer,
        responses={201: CreateAccountResponseSerializer},
    ),
)(AccountListCreateView)


AccountRetrieveUpdateDestroyView = extend_schema_view(
    get=extend_schema(
        tags=['Accounts'],
        summary='Detalhes da conta',
        description='Detalha uma conta específica.',
        responses={200: AccountResponseSerializer}
    ),

    put=extend_schema(
        tags=['Accounts'],
        summary='Atualizar conta',
        description='Atualiza uma conta do usuário.',
        request=UpdateAccountRequestSerializer,
        responses={200: AccountResponseSerializer},
    ),

    patch=extend_schema(
        tags=['Accounts'],
        summary='Atualizar conta',
        description='Atualiza uma conta do usuário.',
        request=UpdateAccountRequestSerializer,
        responses={200: AccountResponseSerializer},
    ),

    delete=extend_schema(
        tags=['Accounts'],
        summary='Detela uma conta',
        description='Delata uma conta específica.',
        responses={204: None}
    )
)(AccountRetrieveUpdateDestroyView)

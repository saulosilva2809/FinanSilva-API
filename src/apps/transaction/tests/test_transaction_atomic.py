import pytest
from decimal import Decimal

from apps.account.models import AccountModel
from apps.authentication.models import UserModel
from apps.transaction.models import TransactionModel
from apps.transaction.services import TransactionService


@pytest.mark.django_db
def test_create_transaction_atomic_and_idempotent():
    """
    Testa:
    - create_transaction aplica saldo corretamente
    - retry NÃO duplica saldo
    - atomic protege contra inconsistência
    """

    user = UserModel.objects.create(
        username='Usuário de Teste',
        email='usertest@gmail.com',
    )

    # cria conta
    account = AccountModel.objects.create(
        user=user,
        name="Conta Teste",
        balance=Decimal("0.00")
    )

    # cria transação
    tx = TransactionModel.objects.create(
        account=account,
        type_transaction="RECEITA",
        value=Decimal("100.00"),
    )

    # primeira execução
    TransactionService.create_transaction(tx)

    account.refresh_from_db()
    assert account.balance == Decimal("100.00")

    # retry (simula erro de rede / timeout / refresh do browser)
    TransactionService.create_transaction(tx)

    account.refresh_from_db()

    # saldo NÃO pode duplicar
    assert account.balance == Decimal("100.00")


@pytest.mark.django_db
def test_atomic_rollback_on_error(monkeypatch):
    """
    Testa se transaction.atomic faz rollback quando explode
    """

    user = UserModel.objects.create(
        username='Usuário de Teste',
        email='usertest@gmail.com',
    )

    account = AccountModel.objects.create(
        user=user,
        name="Conta Crash",
        balance=Decimal("0.00")
    )

    tx = TransactionModel.objects.create(
        account=account,
        type_transaction="RECEITA",
        value=Decimal("200.00"),
    )

    # força erro no meio do processo
    def crash(*args, **kwargs):
        raise Exception("💥 ERRO SIMULADO")

    monkeypatch.setattr(AccountModel, "save", crash)

    with pytest.raises(Exception):
        TransactionService.create_transaction(tx)

    account.refresh_from_db()

    # saldo NÃO pode ter sido alterado
    assert account.balance == Decimal("0.00")

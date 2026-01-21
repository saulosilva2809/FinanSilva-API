from django.db import transaction
from django.utils import timezone

from apps.account.email_messages import message_create_account, message_delete_account
from apps.base.tasks import send_email_task


class AccountService:
    def create_account(self, account_instance):
        first_name = account_instance.user.first_name
        email = account_instance.user.email
        created_at = timezone.localtime(account_instance.created_at)

        message = message_create_account(
            first_name,
            account_instance.name,
            account_instance.bank,
            account_instance.initial_balance,
            created_at.strftime('%d/%m/%Y, %H:%M')
        )

        transaction.on_commit(
            lambda: send_email_task.delay(
                subject=message['email_subject'],
                message=message['email_body'],
                recipient_list=[email]
            )
        )

    def delete_account(self, account_instance):
        first_name = account_instance.user.first_name
        email = account_instance.user.email
        deleted_at = timezone.localtime(timezone.now())

        message = message_delete_account(
            first_name,
            account_instance.name,
            account_instance.bank,
            deleted_at.strftime('%d/%m/%Y, %H:%M')
        )

        transaction.on_commit(
            lambda: send_email_task.delay(
                subject=message['email_subject'],
                message=message['email_body'],
                recipient_list=[email]
            )
        )

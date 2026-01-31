from django.db import transaction
from django.utils import timezone

from apps.authentication.email_messages import message_register, message_update_profile
from apps.base.tasks import send_email_task


class UserService():
    # REGISTRAR USUÁRIO
    def register_user(self, user_instance):
        first_name = user_instance.first_name
        email = user_instance.email
        date_joined = timezone.localtime(user_instance.date_joined)

        message = message_register(
            first_name if first_name else email,
            email,
            date_joined.strftime('%d/%m/%Y, %H:%M'),
        )

        transaction.on_commit(
                lambda: send_email_task.delay(
                subject=message['email_subject'],
                message=message['email_body'],
                recipient_list=[email]
            )
        )

    # ATUALIZAR USUÁRIO
    def update_user(self, user_instance, serializer):
        changes = self._get_changes(user_instance, serializer)
        if changes:
            self._save_updated_at_in_user(user_instance)
            self._send_email(user_instance, changes)

        return user_instance

    def _get_changes(self, user_instance, serializer):
        changes = {}

        for field, value in serializer.validated_data.items():
            old_value = getattr(user_instance, field) # user_instance.nome_do_field
            if old_value != value:
                changes[field] = {"de": old_value, "para": value}

        serializer.save()
        
        return changes
    
    def _save_updated_at_in_user(self, user_instance):
        user_instance.updated_at = timezone.now()
        user_instance.save(update_fields=['updated_at'])

    def _send_email(self, user_instance, changes: dict):
        user_instance.refresh_from_db()

        first_name = user_instance.first_name
        email = user_instance.email
        updated_at = timezone.localtime(user_instance.updated_at)

        message = message_update_profile(
            first_name if first_name else email,
            changes,
            updated_at.strftime('%d/%m/%Y, %H:%M'),
        )

        transaction.on_commit(
            lambda: send_email_task.delay(
                subject=message['email_subject'],
                message=message['email_body'],
                recipient_list=[email]
            )
        )

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=30, retry_kwargs={'max_retries': 5})
def send_emai_task(self, subject: str, message: str, recipient_list: list):
    send_mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        subject=subject,
        message=message,
        recipient_list=recipient_list,
        fail_silently=False,
    )

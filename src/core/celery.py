import os
from celery import Celery

# Garante que o Django esteja configurado antes de iniciar o Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Nome do app Celery (prefixo de tasks e filas)
app = Celery("finansilva")

# Carrega configurações a partir do Django, usando namespace CELERY_*
app.config_from_object("django.conf:settings", namespace="CELERY")

# Descobre tasks em apps Django instaladas que tenham tasks.py
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
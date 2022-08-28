from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes.settings')

app = Celery('quotes')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


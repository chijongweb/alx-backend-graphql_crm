from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings module for 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')

# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# Celery Beat Schedule
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'generate-crm-report': {
        'task': 'crm.tasks.generate_crm_report',
        'schedule': crontab(day_of_week='mon', hour=6, minute=0),
    },
}
# Create Celery app
app = Celery('crm')

# Load settings from Django settings file using CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks from all registered Django app configs
app.autodiscover_tasks()

# Optional: debug log to confirm task discovery
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
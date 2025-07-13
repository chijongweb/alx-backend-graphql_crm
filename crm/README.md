# CRM Scheduled Reporting Setup

## Requirements

- Redis installed and running on localhost:6379
- Python virtual environment activated
- Required packages in `requirements.txt` installed

## Setup Instructions

1. Run migrations:
   ```bash
   python manage.py migrate
-Start Redis server (if not running):
redis-server

-Start Celery worker:
celery -A crm worker -l info

-Start Celery Beat scheduler:
celery -A crm beat -l info

-Check logs at:

/tmp/crm_report_log.txt

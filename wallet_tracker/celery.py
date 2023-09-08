import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wallet_tracker.settings')

app = Celery('wallet_tracker')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# celery beat tasks
app.conf.beat_schedule = {
    'update wallets txs': {
        'task': 'wallets.tasks.update_all_wallets_txs',
        'schedule': crontab(minute='*/5')
    }
}

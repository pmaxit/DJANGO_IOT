from celery.schedules import crontab


SCHEDULE = {
    'refresh_all': {
        'task': 'django_iot.apps.interactions.tasks.refresh_all',
        'schedule': crontab(minute='*/5')
    },

}

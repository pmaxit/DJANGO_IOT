web: gunicorn django_iot.wsgi --log-file -
scheduler: celery worker -B -A django_iot -l info

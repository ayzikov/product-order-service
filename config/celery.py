# base
import os
# installed
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('backend')
# указываем что настройки для Celery будем брать из namespace='CELERY' в settings
app.config_from_object('django.conf:settings', namespace='CELERY')
# автоматически ищем файлы tasks.py во всех приложениях Django
app.autodiscover_tasks()
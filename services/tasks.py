# installed
from celery import shared_task
# local
from .email import send_verifi_mail


@shared_task
def send_verifi_mail_task(current_domain, buyer_id):
    return send_verifi_mail(current_domain, buyer_id)
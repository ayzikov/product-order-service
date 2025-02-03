# installed
from celery import shared_task
# local
from apps.orderserviceapi.services.email import send_verifi_mail, send_order_mail


@shared_task
def send_verifi_mail_task(current_domain, buyer_id):
    return send_verifi_mail(current_domain, buyer_id)

@shared_task
def send_order_mail_task(buyer_id):
    return send_order_mail(buyer_id)
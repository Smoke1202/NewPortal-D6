from allauth.account.signals import email_confirmed
from django.db.models.signals import post_save
from django.dispatch import receiver # импортируем нужный декоратор
from django.core.mail import mail_managers, send_mail
from .models import Appointment


@receiver(post_save, sender=Appointment)
def notify_managers_appointment(sender, instance, created, **kwargs):
    if created:
        subject = f'{instance.client_name}'
    else:
        subject = f'Appointment changed for {instance.client_name}'

    mail_managers(
        subject=subject,
        message=instance.message,
    )

@receiver(email_confirmed)
def user_signed_up(request, email_address, **kwargs):
    # отправляется письмо пользователю, чья почта была подтверждена
    send_mail(
        subject=f'Dear {email_address.user} Welcome to my News Portal!',
        message=f'Приветствую Вас на моём новостном портале. Здесь самые последние новости из разных категорий',
        from_email='Christopherga@yandex.ru',
        recipient_list=[email_address.user.email]
    )
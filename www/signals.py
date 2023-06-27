from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student


@receiver(post_save, sender=Student)
def send_email_on_user_creation(sender, instance, created, **kwargs):
    send_mail(
        subject='School',
        message='You have been added to the school database.',
        from_email='kenwaynoreply@yandex.ru',
        recipient_list=[instance.email]
    )

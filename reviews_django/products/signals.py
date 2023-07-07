from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Profile, Suggestion, Product


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Suggestion)
def send_email_on_suggestion(sender, instance, created, **kwargs):
    if created:
        subject = 'Vaperate | Получен новый предложенный отзыв'
        message = f'Пользователь {instance.author.username} предложил новый отзыв {instance.name}.\n\nhttps://vaperate.ru/dashboard/suggestions'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [settings.ADMIN_EMAIL]
        send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=Product)
def send_email_on_liquid(sender, instance, created, **kwargs):
    if created and not instance.added_by.is_superuser:
        subject = 'Vaperate | Получена новая предложенная жидкость'
        message = f'Получена новая предложенная жидкость {instance.name}.\n\nhttps://vaperate.ru/dashboard/liquids'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [settings.ADMIN_EMAIL]
        send_mail(subject, message, from_email, recipient_list)
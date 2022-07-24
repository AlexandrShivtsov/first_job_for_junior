from django.db.models.signals import pre_save
from django.dispatch import receiver
from accounts.models import User


@receiver(pre_save, sender=User)
def update_user_phone(sender, instance, **kwargs):
    if instance.phone:
        instance.phone = ''.join(dig for dig in instance.phone if dig.isdigit())






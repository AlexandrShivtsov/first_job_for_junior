from django.contrib.auth.models import AbstractUser
from django.db import models

'''cоздаем путь и название загружаемых файлов'''


def upload_to(instance, filename):
    return f'avatars/{instance.id}/{filename}'


class User(AbstractUser):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    avatar = models.FileField(
        blank=True,
        null=True,
        default=None,
        upload_to=upload_to
    )

    phone = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        default=None,
    )

    email = models.EmailField(("email address"), blank=True, unique=True)

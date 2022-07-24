# Generated by Django 4.0.4 on 2022-07-08 17:32

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.FileField(blank=True, default=None, null=True, upload_to=accounts.models.upload_to),
        ),
    ]
# Generated by Django 4.1.7 on 2023-04-27 06:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_rename_is_verifed_user_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='sms',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
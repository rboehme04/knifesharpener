# Generated by Django 3.1.7 on 2021-11-20 20:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knivesharpener', '0002_mail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='read',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]

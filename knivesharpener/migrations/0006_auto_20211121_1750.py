# Generated by Django 3.1.7 on 2021-11-21 16:50

from django.db import migrations
import knivesharpener.models


class Migration(migrations.Migration):

    dependencies = [
        ('knivesharpener', '0005_auto_20211121_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='timestamp',
            field=knivesharpener.models.CustomDateTimeField(auto_now_add=True),
        ),
    ]
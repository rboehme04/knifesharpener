# Generated by Django 3.1.7 on 2021-11-30 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knivesharpener', '0007_cart_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='animation_id',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]

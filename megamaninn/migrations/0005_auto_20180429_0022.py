# Generated by Django 2.0.4 on 2018-04-28 19:22

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('megamaninn', '0004_auto_20180428_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='url',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='room picture'),
        ),
    ]
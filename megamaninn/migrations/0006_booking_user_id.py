# Generated by Django 2.0.4 on 2018-04-29 13:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('megamaninn', '0005_auto_20180429_0022'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]

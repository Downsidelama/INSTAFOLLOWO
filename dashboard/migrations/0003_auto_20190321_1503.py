# Generated by Django 2.1.7 on 2019-03-21 14:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_instagramaccount_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagramaccount',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

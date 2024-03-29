# Generated by Django 3.2.15 on 2023-03-16 17:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0030_serviceuser_is_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotation',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='annotations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owns', to=settings.AUTH_USER_MODEL),
        ),
    ]

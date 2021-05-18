# Generated by Django 3.2 on 2021-04-30 13:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_alter_serviceuser_owns'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceuser',
            name='owns',
        ),
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owns', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='data',
            field=models.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='document',
            name='data',
            field=models.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='project',
            name='data',
            field=models.JSONField(default={}),
        ),
    ]
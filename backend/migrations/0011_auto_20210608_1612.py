# Generated by Django 3.2 on 2021-06-08 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_auto_20210604_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='timed_out',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='annotation_timeout',
            field=models.IntegerField(default=60),
        ),
    ]
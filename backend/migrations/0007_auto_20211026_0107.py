# Generated by Django 3.2 on 2021-10-26 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_auto_20211020_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='annotator_guideline',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='project',
            name='document_input_preview',
            field=models.JSONField(default={}),
        ),
    ]

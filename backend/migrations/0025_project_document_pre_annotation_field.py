# Generated by Django 3.2.15 on 2022-11-01 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0024_rename_data_annotation__data'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='document_pre_annotation_field',
            field=models.TextField(default=''),
        ),
    ]
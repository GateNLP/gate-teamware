# Generated by Django 3.2 on 2022-03-25 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0017_document_doc_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='document_gold_standard_field',
            field=models.TextField(default='gold'),
        ),
    ]

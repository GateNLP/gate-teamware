# Generated by Django 3.2 on 2021-10-26 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_alter_project_document_input_preview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='document_input_preview',
            field=models.JSONField(default={'text': '<p>Some html text <strong>in bold</strong>.</p><p>Paragraph 2.</p>'}),
        ),
    ]

# Generated by Django 3.2.8 on 2022-03-18 16:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_annotation_time_to_complete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceuser',
            name='annotates',
        ),
        migrations.AddField(
            model_name='project',
            name='can_annotate_after_passing_test',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='project',
            name='has_test_stage',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='has_training_stage',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='min_test_pass_threshold',
            field=models.FloatField(default=1.0, null=True),
        ),
        migrations.CreateModel(
            name='AnnotatorProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('training_score', models.FloatField(null=True)),
                ('test_score', models.FloatField(null=True)),
                ('training_completed', models.DateTimeField(null=True)),
                ('test_completed', models.DateTimeField(null=True)),
                ('annotations_completed', models.DateTimeField(null=True)),
                ('status', models.IntegerField(choices=[(0, 'Active'), (1, 'Completed')], default=0)),
                ('annotator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.project')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='annotators',
            field=models.ManyToManyField(related_name='annotates', through='backend.AnnotatorProject', to=settings.AUTH_USER_MODEL),
        ),
    ]

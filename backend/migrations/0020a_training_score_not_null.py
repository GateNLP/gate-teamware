from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0020_auto_20220330_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotatorproject',
            name='training_score',
            field=models.FloatField(default=0),
        ),
    ]


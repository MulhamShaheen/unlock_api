# Generated by Django 3.2.5 on 2022-06-16 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ScoreManager', '0003_alter_person_middle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='middle',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]

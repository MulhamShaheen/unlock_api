# Generated by Django 3.2.5 on 2022-06-30 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ScoreManager', '0007_auto_20220619_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
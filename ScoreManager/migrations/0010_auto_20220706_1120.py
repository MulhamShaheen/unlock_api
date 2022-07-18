# Generated by Django 3.2.5 on 2022-07-06 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ScoreManager', '0009_auto_20220630_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScoreLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(default=0.5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ScoreManager.event')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ScoreManager.person')),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='attendance',
        ),
        migrations.AddField(
            model_name='event',
            name='attendance',
            field=models.ManyToManyField(through='ScoreManager.ScoreLog', to='ScoreManager.Person'),
        ),
    ]

# Generated by Django 4.0.2 on 2022-05-27 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moshavere', '0022_days_times'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='time',
        ),
        migrations.AddField(
            model_name='reservation',
            name='time',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='moshavere.time'),
        ),
    ]

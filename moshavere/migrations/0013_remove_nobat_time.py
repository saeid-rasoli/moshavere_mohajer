# Generated by Django 4.0.2 on 2022-05-16 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moshavere', '0012_reservation_tarikh'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nobat',
            name='time',
        ),
    ]

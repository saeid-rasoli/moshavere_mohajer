# Generated by Django 4.0.2 on 2022-05-22 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moshavere', '0019_alter_consulation_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='time',
            field=models.CharField(blank=True, choices=[('۸:۰۰', '۸:۰۰'), ('۹:۰۰', '۹:۰۰'), ('۱۰:۰۰', '۱۰:۰۰'), ('۱۱:۰۰', '۱۱:۰۰')], max_length=40, null=True),
        ),
    ]

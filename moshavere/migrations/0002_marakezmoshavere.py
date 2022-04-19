# Generated by Django 4.0.2 on 2022-04-12 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moshavere', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarakezMoshavere',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('markaz_name', models.CharField(blank=True, max_length=400, null=True)),
                ('daneshgah_code', models.CharField(blank=True, max_length=50, null=True)),
                ('karbari_markaz_behdasht', models.CharField(blank=True, max_length=80, null=True)),
                ('karbari_markaz_moshavere', models.CharField(blank=True, max_length=80, null=True)),
            ],
        ),
    ]
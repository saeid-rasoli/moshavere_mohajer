# Generated by Django 4.0.2 on 2022-04-12 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moshavere', '0003_rename_markaz_name_marakezmoshavere_daneshgah_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]

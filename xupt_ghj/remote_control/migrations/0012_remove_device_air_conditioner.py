# Generated by Django 2.0.2 on 2018-05-09 08:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('remote_control', '0011_remove_device_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='air_conditioner',
        ),
    ]

# Generated by Django 2.0.2 on 2018-05-04 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remote_control', '0006_auto_20180505_0231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='name',
            field=models.CharField(max_length=255, null=True, unique=True, verbose_name='自定义设备名字'),
        ),
    ]

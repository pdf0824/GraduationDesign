# Generated by Django 2.0.2 on 2018-05-15 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sign_in_system', '0009_timetable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='class_name',
            field=models.CharField(max_length=80, unique=True, verbose_name='班级'),
        ),
    ]

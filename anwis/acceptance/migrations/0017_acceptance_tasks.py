# Generated by Django 4.1.2 on 2022-11-25 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('acceptance', '0016_alter_box_box'),
    ]

    operations = [
        migrations.AddField(
            model_name='acceptance',
            name='tasks',
            field=models.ManyToManyField(blank=True, to='common.task', verbose_name='Задачи'),
        ),
    ]

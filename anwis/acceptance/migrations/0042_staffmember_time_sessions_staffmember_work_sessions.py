# Generated by Django 4.1.2 on 2022-12-09 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acceptance', '0041_alter_timesession_break_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffmember',
            name='time_sessions',
            field=models.ManyToManyField(blank=True, to='acceptance.timesession', verbose_name='Временные Сессии'),
        ),
        migrations.AddField(
            model_name='staffmember',
            name='work_sessions',
            field=models.ManyToManyField(blank=True, to='acceptance.worksession', verbose_name='Рабочие Сессии'),
        ),
    ]
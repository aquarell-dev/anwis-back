# Generated by Django 4.1.2 on 2022-12-09 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acceptance', '0042_staffmember_time_sessions_staffmember_work_sessions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acceptance',
            name='cargo_number',
            field=models.CharField(blank=True, max_length=264, null=True, verbose_name='Номер карго'),
        ),
        migrations.AlterField(
            model_name='acceptance',
            name='title',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Название'),
        ),
    ]

# Generated by Django 4.1.2 on 2022-10-29 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('china', '0022_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='tasks',
            field=models.ManyToManyField(blank=True, to='china.task', verbose_name='Задачи'),
        ),
    ]

# Generated by Django 4.1.2 on 2022-10-29 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('china', '0021_rename_icon_status_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.TextField(verbose_name='Задача')),
                ('datetime', models.DateTimeField(verbose_name='Дата и время')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
            },
        ),
    ]
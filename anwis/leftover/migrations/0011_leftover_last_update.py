# Generated by Django 4.1.2 on 2022-11-03 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leftover', '0010_leftover_buffer_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='leftover',
            name='last_update',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

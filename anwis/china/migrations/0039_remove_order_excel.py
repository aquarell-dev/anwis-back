# Generated by Django 4.1.2 on 2022-11-06 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('china', '0038_order_excel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='excel',
        ),
    ]

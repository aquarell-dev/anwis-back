# Generated by Django 4.1.2 on 2022-11-24 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acceptance', '0013_productspecification_actual_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='acceptance',
            old_name='products',
            new_name='specifications',
        ),
    ]

# Generated by Django 4.1.2 on 2022-12-07 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acceptance', '0037_box_finished'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Session',
            new_name='WorkSession',
        ),
        migrations.RenameField(
            model_name='staffmember',
            old_name='session',
            new_name='work_session',
        ),
    ]

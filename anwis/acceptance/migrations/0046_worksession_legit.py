# Generated by Django 4.1.2 on 2022-12-11 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acceptance', '0045_remove_worksession_quantity_worksession_box'),
    ]

    operations = [
        migrations.AddField(
            model_name='worksession',
            name='legit',
            field=models.BooleanField(default=False, verbose_name='Учитывать сессию'),
        ),
    ]
# Generated by Django 4.1.2 on 2022-12-11 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acceptance', '0046_worksession_legit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worksession',
            name='legit',
            field=models.BooleanField(default=True, verbose_name='Учитывать сессию'),
        ),
    ]

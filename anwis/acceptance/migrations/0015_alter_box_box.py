# Generated by Django 4.1.2 on 2022-11-24 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acceptance', '0014_rename_products_acceptance_specifications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='box',
            name='box',
            field=models.CharField(max_length=24, unique=True, verbose_name='Номер Коробки'),
        ),
    ]

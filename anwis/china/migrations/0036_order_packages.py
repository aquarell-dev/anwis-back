# Generated by Django 4.1.2 on 2022-11-06 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('china', '0035_alter_product_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='packages',
            field=models.PositiveIntegerField(default=0, verbose_name='Кол-во грузовых мест'),
        ),
    ]
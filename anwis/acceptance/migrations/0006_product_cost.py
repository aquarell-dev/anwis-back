# Generated by Django 4.1.2 on 2022-11-14 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acceptance', '0005_acceptancecategory_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cost',
            field=models.FloatField(blank=True, null=True, verbose_name='Себестоимость'),
        ),
    ]

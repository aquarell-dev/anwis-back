# Generated by Django 4.1.2 on 2022-11-14 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acceptance', '0005_acceptancecategory_product'),
        ('china', '0051_alter_product_category'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductQuantity',
            new_name='ProductInfo',
        ),
    ]

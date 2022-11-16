# Generated by Django 4.1.2 on 2022-11-14 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acceptance', '0008_acceptance_linked_china_product_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='cost',
            new_name='last_cost',
        ),
        migrations.RemoveField(
            model_name='acceptance',
            name='linked_china_product',
        ),
        migrations.AddField(
            model_name='product',
            name='linked_china_product_article',
            field=models.CharField(blank=True, editable=False, max_length=100, null=True, verbose_name='Артикул Китайского Товара'),
        ),
        migrations.AddField(
            model_name='product',
            name='linked_china_product_size',
            field=models.CharField(blank=True, editable=False, max_length=100, null=True, verbose_name='Размер Китайского Товара'),
        ),
        migrations.AddField(
            model_name='productspecification',
            name='cost',
            field=models.FloatField(blank=True, null=True, verbose_name='Себестоимость'),
        ),
    ]

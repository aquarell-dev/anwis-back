# Generated by Django 4.1.2 on 2022-11-16 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acceptance', '0009_rename_cost_product_last_cost_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productspecification',
            options={'verbose_name': 'Информация о Продукте', 'verbose_name_plural': 'Информация о Продуктах'},
        ),
        migrations.AddField(
            model_name='acceptance',
            name='from_order',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Создан из заказа'),
        ),
        migrations.AlterField(
            model_name='product',
            name='linked_china_product_article',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Артикул Китайского Товара'),
        ),
        migrations.AlterField(
            model_name='product',
            name='linked_china_product_size',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Размер Китайского Товара'),
        ),
    ]

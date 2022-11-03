# Generated by Django 4.1.2 on 2022-11-02 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('china', '0029_order_in_moscow_date_order_shipping_from_china_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cargo_number',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Номер Доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='cargo_volume',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Объем карго'),
        ),
        migrations.AlterField(
            model_name='order',
            name='cargo_weight',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Вес карго'),
        ),
        migrations.AlterField(
            model_name='order',
            name='package_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Цена упаковки, $'),
        ),
        migrations.AlterField(
            model_name='order',
            name='price_per_kg',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Цена за кг, $'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_delivery',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Цена за доствку, $'),
        ),
    ]
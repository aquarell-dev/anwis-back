# Generated by Django 4.1.2 on 2022-11-08 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('china', '0043_order_documents_alter_product_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='course',
            field=models.FloatField(default=0, verbose_name='Курс'),
        ),
        migrations.AlterField(
            model_name='order',
            name='package_price',
            field=models.FloatField(default=0, verbose_name='Цена упаковки, $'),
        ),
        migrations.AlterField(
            model_name='order',
            name='price_per_kg',
            field=models.FloatField(default=0, verbose_name='Цена за кг, $'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_cny',
            field=models.FloatField(default=0, verbose_name='Сумма в юанях'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_delivery',
            field=models.FloatField(default=0, verbose_name='Цена за доствку, $'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_expenses',
            field=models.FloatField(default=0, verbose_name='Доп. расходы в рублях'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_rub',
            field=models.FloatField(default=0, verbose_name='Сумма в юанях'),
        ),
    ]

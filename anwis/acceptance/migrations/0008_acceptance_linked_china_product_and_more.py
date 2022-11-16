# Generated by Django 4.1.2 on 2022-11-14 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acceptance', '0007_productspecification_alter_acceptance_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='acceptance',
            name='linked_china_product',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='АйДи Китайского Товара'),
        ),
        migrations.AlterField(
            model_name='acceptance',
            name='products',
            field=models.ManyToManyField(blank=True, to='acceptance.productspecification', verbose_name='Товары'),
        ),
    ]
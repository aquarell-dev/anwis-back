# Generated by Django 4.1.2 on 2022-12-13 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('china', '0056_alter_order_individual_entrepreneur_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinfo',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='china.product', verbose_name='Продукт'),
        ),
    ]
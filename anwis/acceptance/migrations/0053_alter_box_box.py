# Generated by Django 4.1.2 on 2022-12-20 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acceptance', '0052_remove_product_wb_article_product_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='box',
            name='box',
            field=models.CharField(blank=True, max_length=24, verbose_name='Номер Коробки'),
        ),
    ]

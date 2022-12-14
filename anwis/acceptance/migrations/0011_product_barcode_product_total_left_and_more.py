# Generated by Django 4.1.2 on 2022-11-16 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acceptance', '0010_alter_productspecification_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='barcode',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Штрих-код'),
        ),
        migrations.AddField(
            model_name='product',
            name='total_left',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Остаток'),
        ),
        migrations.AddField(
            model_name='product',
            name='wb_article',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Артикул ВБ'),
        ),
    ]

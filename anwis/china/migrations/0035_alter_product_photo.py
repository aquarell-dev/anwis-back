# Generated by Django 4.1.2 on 2022-11-05 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('china', '0034_product_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Картинка'),
        ),
    ]
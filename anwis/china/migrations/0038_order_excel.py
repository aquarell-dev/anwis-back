# Generated by Django 4.1.2 on 2022-11-06 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('china', '0037_alter_product_article_alter_product_size_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='excel',
            field=models.FileField(default=1, upload_to='documents/auto/', verbose_name='Эксель'),
            preserve_default=False,
        ),
    ]

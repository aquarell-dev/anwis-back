# Generated by Django 4.1.2 on 2022-12-03 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('acceptance', '0030_box_worker'),
    ]

    operations = [
        migrations.AddField(
            model_name='box',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='acceptance.product', verbose_name='Товар'),
        ),
    ]

# Generated by Django 4.1.2 on 2022-10-31 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leftover', '0004_alter_leftover_detailed_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leftover',
            name='detailed_data',
            field=models.ManyToManyField(blank=True, editable=False, to='leftover.leftoverdetaileddata', verbose_name='Детальные данные'),
        ),
    ]

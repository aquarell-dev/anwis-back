# Generated by Django 4.1.2 on 2022-10-21 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('china', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterField(
            model_name='order',
            name='china_distributor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='china.chinadistributor', verbose_name='Китайский посредник'),
        ),
        migrations.AlterField(
            model_name='order',
            name='commentary',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='order',
            name='individual_entrepreneur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='china.individualentrepreneur', verbose_name='Индивидуальный предприниматель'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_for_project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='china.orderforproject', verbose_name='Заказ под проект'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='china.status', verbose_name='Статус'),
        ),
    ]

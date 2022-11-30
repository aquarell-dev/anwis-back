# Generated by Django 4.1.2 on 2022-11-28 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
        ('acceptance', '0020_reason_productspecification_reasons'),
    ]

    operations = [
        migrations.AddField(
            model_name='acceptance',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий'),
        ),
        migrations.AddField(
            model_name='acceptance',
            name='documents',
            field=models.ManyToManyField(blank=True, to='documents.document', verbose_name='Документы'),
        ),
    ]

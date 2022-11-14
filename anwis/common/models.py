from django.db import models


class CommonCategory(models.Model):
    category = models.CharField('Категория', unique=True, max_length=60)

    class Meta:
        abstract = True


class CommonProduct(models.Model):
    title = models.CharField('Название товара', max_length=100)
    article = models.CharField('Артикул поставщика', max_length=100)
    color = models.CharField('Цвет', max_length=100)
    size = models.CharField('Размер', max_length=100, blank=True, null=True)
    brand = models.CharField('Брэнд', max_length=100)

    class Meta:
        abstract = True

from django.db import models


class LeftOverDetailedData(models.Model):
    title = models.CharField(max_length=64)
    quantity = models.PositiveIntegerField()


class LeftOver(models.Model):
    title = models.CharField('Название товара', max_length=256, editable=False)
    url = models.URLField('Ссылка на товар')
    photo_url = models.URLField('Ссылка на фото товара')
    nm = models.CharField('Номер товара', unique=True, max_length=64, editable=False)
    products = models.ManyToManyField(LeftOverDetailedData, verbose_name='Детальные данные', blank=True,
                                           editable=False)
    total = models.PositiveIntegerField('Всего товара', default=0)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Остаток'
        verbose_name_plural = 'Остатки'

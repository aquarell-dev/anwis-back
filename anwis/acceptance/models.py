from django.db import models


class Acceptance(models.Model):
    title = models.CharField('Название', max_length=64)
    cargo_number = models.CharField('Номер карго', max_length=264)
    cargo_volume = models.CharField('Объем карго', null=True, blank=True, max_length=256)
    cargo_weight = models.CharField('Вес карго', null=True, blank=True, max_length=256)
    arrived_in_moscow = models.DateField('Дата приезда в Москву', blank=True, null=True)
    shipped_from_china = models.DateField('Дата отправки из Китая', blank=True, null=True)
    products = models.ManyToManyField('china.ProductQuantity', blank=True)
    custom_id = models.CharField(unique=True, max_length=10, editable=False, blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return f'Приемка №{self.id}'

    class Meta:
        verbose_name = 'Приемка'
        verbose_name_plural = 'Приемки'

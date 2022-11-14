from django.db import models

from common.models import CommonProduct, CommonCategory
from documents.models import Photo


class Acceptance(models.Model):
    title = models.CharField('Название', max_length=64)
    cargo_number = models.CharField('Номер карго', max_length=264)
    cargo_volume = models.CharField('Объем карго', null=True, blank=True, max_length=256)
    cargo_weight = models.CharField('Вес карго', null=True, blank=True, max_length=256)
    arrived_in_moscow = models.DateField('Дата приезда в Москву', blank=True, null=True)
    shipped_from_china = models.DateField('Дата отправки из Китая', blank=True, null=True)
    products = models.ManyToManyField('china.ProductInfo', blank=True)
    custom_id = models.CharField(unique=True, max_length=10, editable=False, blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return f'Приемка №{self.id}'

    class Meta:
        verbose_name = 'Приемка'
        verbose_name_plural = 'Приемки'


class StaffMember(models.Model):
    username = models.CharField('Юзер', max_length=264, unique=True)
    password = models.CharField('Пароль', max_length=264)
    inactive = models.BooleanField('Деактивирован', default=False)
    temporary = models.BooleanField('Временный', default=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class AcceptanceCategory(CommonCategory):
    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(CommonProduct):
    photo = models.ForeignKey(Photo, verbose_name='Картинка', blank=True, null=True, on_delete=models.SET_NULL,
                              related_name='acceptance_photo_product')
    category = models.ForeignKey(AcceptanceCategory, verbose_name='Категория', on_delete=models.SET_NULL, blank=True,
                                 null=True)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

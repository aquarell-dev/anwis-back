from datetime import datetime

from django.db import models

from common.models import CommonProduct, CommonCategory, Task, Project, IndividualEntrepreneur
from documents.models import Photo, Document


class AcceptanceCategory(CommonCategory):
    payment_options = (
        ('hourly', 'Почасовая'),
        ('apiece', 'Поштучно')
    )

    payment = models.CharField('Оплата', choices=payment_options, max_length=64, blank=True, null=True)
    per_hour = models.FloatField('За час', blank=True, null=True)
    per_piece = models.FloatField('За штуку', blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Reason(models.Model):
    reason = models.CharField('Причина', max_length=100, blank=True)
    quantity = models.PositiveSmallIntegerField('Количество')

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'Причина'
        verbose_name_plural = 'Причины'


class Product(CommonProduct):
    photo = models.ForeignKey(Photo, verbose_name='Картинка', blank=True, null=True, on_delete=models.SET_NULL,
                              related_name='acceptance_photo_product')
    category = models.ForeignKey(AcceptanceCategory, verbose_name='Категория', on_delete=models.SET_NULL, blank=True,
                                 null=True)
    last_cost = models.FloatField('Себестоимость', blank=True, null=True)
    barcode = models.CharField('Штрих-код', max_length=100, null=True, blank=True)
    wb_article = models.CharField('Артикул ВБ', max_length=100, null=True, blank=True)
    linked_china_product_article = models.CharField('Артикул Китайского Товара', max_length=100, blank=True, null=True)
    linked_china_product_size = models.CharField('Размер Китайского Товара', max_length=100, blank=True, null=True)
    total_left = models.PositiveIntegerField('Остаток', null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ProductSpecification(models.Model):
    quantity = models.PositiveSmallIntegerField('Количество товаров')
    actual_quantity = models.PositiveSmallIntegerField('Фактическое Количество Товаров', blank=True, null=True)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    cost = models.FloatField('Себестоимость', blank=True, null=True)
    boxes = models.ManyToManyField('Box', verbose_name='Коробки', blank=True)
    reasons = models.ManyToManyField(Reason, verbose_name='Причины', blank=True)

    def __str__(self):
        return f'{self.product.title}, {self.cost}, {self.quantity}'

    class Meta:
        verbose_name = 'Информация о Продукте'
        verbose_name_plural = 'Информация о Продуктах'


class AcceptanceStatus(models.Model):
    status = models.CharField('Статус', unique=True, max_length=100)
    color = models.CharField('Цвет', help_text='Цвет на фронте', max_length=40)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Session(models.Model):
    start = models.DateTimeField('Время Начала', default=datetime.now, blank=True)
    end = models.DateTimeField('Время Конца', null=True, blank=True)

    class Meta:
        abstract = True


class WorkSession(Session):
    #  Сессия по коробкам # TODO переименовать
    box = models.ForeignKey('Box', verbose_name='Коробка', on_delete=models.CASCADE)
    legit = models.BooleanField('Учитывать сессию', default=True)

    def __str__(self):
        return f'{self.box} - {self.start} -> {self.end}'

    class Meta:
        verbose_name = 'Рабочая Сессия'
        verbose_name_plural = 'Рабочая Сессии'


class TimeSession(Session):
    break_start = models.DateTimeField('Время Начала Перерыва', null=True, blank=True)
    break_end = models.DateTimeField('Время Конца Перерыва', null=True, blank=True)

    def __str__(self):
        return f'{self.start} -> {self.end}'

    class Meta:
        verbose_name = 'Сессия По Времени'
        verbose_name_plural = 'Сессии По Времени'


class Box(models.Model):
    box = models.CharField('Номер Коробки', max_length=24)
    quantity = models.PositiveIntegerField('Кол-во товаров в коробке')
    specification = models.ForeignKey(
        ProductSpecification,
        verbose_name='Информация О Товаре',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    archive = models.BooleanField('Архивная Коробка', default=False)
    finished = models.BooleanField('Закончена', default=False)

    def __str__(self):
        return self.box

    class Meta:
        verbose_name = 'Коробка'
        verbose_name_plural = 'Коробки'


class Payment(models.Model):
    paid_break = models.PositiveSmallIntegerField('Оплачиваемый Перерыв', help_text='В минутах', default=0)
    hour_cost = models.PositiveSmallIntegerField('Стоимость Одного Часа Сотрудника', help_text='В рублях', default=0)

    def __str__(self):
        return 'Оплата'

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплата'


class StaffMember(models.Model):
    username = models.CharField('Юзер', max_length=264, unique=True)
    password = models.CharField('Пароль', max_length=264)
    inactive = models.BooleanField('Деактивирован', default=False)
    temporary = models.BooleanField('Временный', default=False)
    unique_number = models.CharField('Уникальный Номер', unique=True, max_length=64, null=True, blank=True)
    box = models.ForeignKey(Box, verbose_name='Коробка', on_delete=models.SET_NULL, blank=True, null=True)
    work_session = models.ForeignKey(WorkSession, verbose_name='Сессия По Коробкам', on_delete=models.SET_NULL,
                                     blank=True, null=True, related_name='work')
    time_session = models.ForeignKey(TimeSession, verbose_name='Сессия По Времени', on_delete=models.SET_NULL,
                                     blank=True, null=True, related_name='time')

    # to keep track of sessions by days, auto-clear after every start of new work
    time_sessions = models.ManyToManyField(TimeSession, verbose_name='Временные Сессии', blank=True)
    work_sessions = models.ManyToManyField(WorkSession, verbose_name='Рабочие Сессии', blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Acceptance(models.Model):
    title = models.CharField('Название', max_length=64, blank=True, null=True)
    cargo_number = models.CharField('Номер карго', max_length=264, blank=True, null=True)
    cargo_volume = models.CharField('Объем карго', null=True, blank=True, max_length=256)
    cargo_weight = models.CharField('Вес карго', null=True, blank=True, max_length=256)
    arrived_in_moscow = models.DateField('Дата приезда в Москву', blank=True, null=True)
    shipped_from_china = models.DateField('Дата отправки из Китая', blank=True, null=True)
    specifications = models.ManyToManyField(ProductSpecification, verbose_name='Товары', blank=True)
    custom_id = models.CharField(unique=True, max_length=10, editable=False, blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', default=datetime.now, blank=True)
    from_order = models.PositiveIntegerField('Создан из заказа', blank=True, null=True)
    tasks = models.ManyToManyField(Task, verbose_name='Задачи', blank=True)
    comment = models.TextField('Комментарий', blank=True, null=True)
    documents = models.ManyToManyField(Document, verbose_name='Документы', blank=True)
    status = models.ForeignKey(AcceptanceStatus, verbose_name='Статус', to_field='status', default='Новая Приемка',
                               on_delete=models.PROTECT)
    project = models.ForeignKey(Project, verbose_name='Проект', on_delete=models.SET_NULL, null=True, blank=True)
    individual = models.ForeignKey(IndividualEntrepreneur, verbose_name='ИП', on_delete=models.SET_NULL, null=True,
                                   blank=True)

    def __str__(self):
        return f'Приемка №{self.id}'

    class Meta:
        verbose_name = 'Приемка'
        verbose_name_plural = 'Приемки'

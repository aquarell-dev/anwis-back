from django.db import models

from documents.models import Photo, Document


class IndividualEntrepreneur(models.Model):
    individual_entrepreneur = models.CharField('ИП', max_length=80, unique=True)

    def __str__(self):
        return str(self.individual_entrepreneur)

    class Meta:
        verbose_name = 'Индивидуальный предприниматель'
        verbose_name_plural = 'Индивидуальные предприниматели'


class ChinaDistributor(models.Model):
    china_distributor = models.CharField('Китайский посредник', max_length=80, unique=True)

    def __str__(self):
        return str(self.china_distributor)

    class Meta:
        verbose_name = 'Китайский посредник'
        verbose_name_plural = 'Китайские посредники'


class OrderForProject(models.Model):
    order_for_project = models.CharField('Заказ под проект', max_length=80, unique=True)

    def __str__(self):
        return str(self.order_for_project)

    class Meta:
        verbose_name = 'Заказ под проект'
        verbose_name_plural = 'Заказы под проекты'


class Status(models.Model):
    status = models.CharField('Статус', unique=True, max_length=50)
    color = models.CharField('Цвет', max_length=40, help_text='Цвет в jsx формате')
    hover_color = models.CharField('Цвет при наведении на блок', max_length=40, help_text='Цвет в jsx формате')
    photo = models.ImageField('Иконка', upload_to='images/')

    def __str__(self):
        return str(self.status)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Category(models.Model):
    category = models.CharField('Категория', unique=True, max_length=60)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    title = models.CharField('Название товара', max_length=100)
    article = models.CharField('Артикул поставщика', max_length=100)
    photo = models.ForeignKey(Photo, verbose_name='Картинка', blank=True, null=True, on_delete=models.SET_NULL)
    color = models.CharField('Цвет', max_length=100)
    size = models.CharField('Размер', max_length=100, blank=True, null=True)
    brand = models.CharField('Брэнд', max_length=100)
    url = models.URLField('Ссылка на товар', blank=True, null=True)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, blank=True,
                                 null=True)

    def __str__(self):
        return f'{self.article}, {self.title}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductQuantity(models.Model):
    quantity = models.PositiveSmallIntegerField('Кол-во товаров')
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)
    price_cny = models.DecimalField('Цена в юанях', decimal_places=2, max_digits=12, default=0)
    cny_to_rub_course = models.DecimalField('Курс юаня к рублю', decimal_places=2, max_digits=12, default=0)
    price_rub = models.DecimalField('Цена в рублях', decimal_places=2, max_digits=12, default=0)
    additional_expenses = models.DecimalField('Доп. расходы в рублях', decimal_places=2, max_digits=12, default=0)

    def __str__(self):
        return f'Продукт - {self.product.title}, кол-во - {self.quantity}'

    class Meta:
        verbose_name = 'Продукт/кол-во'
        verbose_name_plural = 'Продукты/кол-ва'


class Task(models.Model):
    task = models.TextField('Задача')
    datetime = models.DateTimeField('Дата и время')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Order(models.Model):
    individual_entrepreneur = models.ForeignKey(IndividualEntrepreneur,
                                                verbose_name='Индивидуальный предприниматель',
                                                on_delete=models.CASCADE)
    china_distributor = models.ForeignKey(ChinaDistributor, verbose_name='Китайский посредник',
                                          on_delete=models.CASCADE)
    order_for_project = models.ForeignKey(OrderForProject, verbose_name='Заказ под проект',
                                          on_delete=models.CASCADE)
    status = models.ForeignKey(Status, verbose_name='Статус',
                               on_delete=models.CASCADE)
    draft = models.BooleanField('Черновик', default=False)
    commentary = models.TextField('Комментарий', null=True, blank=True)
    date = models.DateTimeField('Дата и время', auto_now_add=True)
    custom_id = models.CharField('Кастомное айди', editable=False, max_length=10)
    tasks = models.ManyToManyField(Task, verbose_name='Задачи', blank=True)
    total_cny = models.DecimalField('Сумма в юанях', decimal_places=2, max_digits=12, default=0)
    total_rub = models.DecimalField('Сумма в юанях', decimal_places=2, max_digits=12, default=0)
    course = models.DecimalField('Курс', decimal_places=2, max_digits=12, default=0)
    total_expenses = models.DecimalField('Доп. расходы в рублях', decimal_places=2, max_digits=12, default=0)
    total_quantity = models.PositiveIntegerField('Кол-во товаров', default=0)
    ready_date = models.DateField('Время изготовления', null=True, blank=True)
    shipping_from_china_date = models.DateField('Дата отправки из китая', null=True, blank=True)
    in_moscow_date = models.DateField('Дата приезда в Москву', null=True, blank=True)
    cargo_number = models.CharField('Номер Доставки', null=True, blank=True, max_length=256)
    cargo_weight = models.CharField('Вес карго', null=True, blank=True, max_length=256)
    cargo_volume = models.CharField('Объем карго', null=True, blank=True, max_length=256)
    price_per_kg = models.DecimalField('Цена за кг, $', decimal_places=2, max_digits=12, default=0)
    package_price = models.DecimalField('Цена упаковки, $', decimal_places=2, max_digits=12, default=0)
    total_delivery = models.DecimalField('Цена за доствку, $', decimal_places=2, max_digits=12, default=0)
    packages = models.PositiveIntegerField('Кол-во грузовых мест', default=0)
    delivered = models.BooleanField('Доставлен', default=False)
    excel = models.FileField('Эксель', upload_to='documents/auto/', blank=True, null=True)
    documents = models.ManyToManyField(Document, verbose_name='Картинки', blank=True)

    products = models.ManyToManyField(ProductQuantity, verbose_name='Товары')

    def __str__(self):
        return f'Заказ №{self.id}'

    def save(self, *args, **kwargs):
        self.custom_id = '0' * (4 - len(str(self.id))) + str(self.id)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'



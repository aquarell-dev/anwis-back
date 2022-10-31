from django.db import models


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
    title = models.CharField('Название товара', max_length=100, unique=True)
    article = models.PositiveBigIntegerField('Артикул')
    photo = models.ImageField('Картинка', upload_to='images/')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, default=1, blank=True,
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
    total_expenses = models.DecimalField('Доп. расходы в рублях', decimal_places=2, max_digits=12, default=0)
    total_quantity = models.PositiveIntegerField('Кол-во товаров', default=0)
    ready_date = models.DateField('Время изготовления', null=True, blank=True)

    products = models.ManyToManyField(ProductQuantity, verbose_name='Товары')

    def __str__(self):
        return f'Заказ №{self.id}'

    def save(self, *args, **kwargs):
        self.custom_id = '0' * (4 - len(str(self.id))) + str(self.id)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

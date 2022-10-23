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
    icon = None

    def __str__(self):
        return str(self.status)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Product(models.Model):
    title = models.CharField('Название товара', max_length=100, unique=True)
    article = models.PositiveBigIntegerField('Артикул')
    price_cny = models.DecimalField('Цена в юанях', decimal_places=2, max_digits=6)
    cny_to_rub_course = models.DecimalField('Курс юаня к рублю', decimal_places=2, max_digits=6)
    price_rub = models.DecimalField('Цена в рублях', decimal_places=2, max_digits=6, editable=False)
    photo = models.ImageField('Картинка', upload_to='images/')

    def save(self, *args, **kwargs):
        self.price_rub = self.price_cny * self.cny_to_rub_course
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    individual_entrepreneur = models.ForeignKey(IndividualEntrepreneur,
                                                verbose_name='Индивидуальный предприниматель',
                                                on_delete=models.CASCADE)
    china_distributor = models.ForeignKey(ChinaDistributor, verbose_name='Китайский посредник',
                                          on_delete=models.CASCADE)
    order_for_project = models.ForeignKey(OrderForProject, verbose_name='Заказ под проект',
                                          on_delete=models.CASCADE)
    photo = None
    status = models.ForeignKey(Status, verbose_name='Статус',
                               on_delete=models.CASCADE)
    draft = models.BooleanField('Черновик', default=False)
    commentary = models.TextField('Комментарий', null=True, blank=True)

    products = models.ManyToManyField(Product, verbose_name='Товары')  # quantity for each, calc prices

    def __str__(self):
        return f'Заказ №{self.id}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

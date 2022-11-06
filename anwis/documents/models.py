from django.db import models


class Document(models.Model):
    title = models.CharField('Название', max_length=264, blank=True, null=True)
    document = models.FileField('Документ', upload_to='documents/')

    def __str__(self):
        return f'Документ {self.id}/{self.title}'

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class Photo(models.Model):
    title = models.CharField('Название', max_length=264, blank=True, null=True)
    photo = models.ImageField('Картинка', upload_to='images/')

    def __str__(self):
        return f'Картинка {self.id}/{self.title}'

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

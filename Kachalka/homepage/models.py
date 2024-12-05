from django.db import models
from datetime import datetime
from .validators import *
from django.utils import timezone

# Create your models here.


class Types(models.Model):
    name = models.CharField('Тип', max_length=32)

    class Meta:
        verbose_name = 'Тип',
        verbose_name_plural = 'Типы'

    def __str__(self):
        return self.name


class Statistic(models.Model):
    date = models.DateField('Дата', validators=(max_date,), default=timezone.now)

    def date_as_string(self):
        return self.date.strftime('%d-%m-%Y')

    calories = models.IntegerField('Калории', validators=(min_cal,))
    time = models.TimeField('Время', validators=(min_time,), default=time(hour=0, minute=0))
    type = models.ForeignKey(
        Types,
        on_delete=models.CASCADE,
        related_name='types',
        verbose_name='Тип',
    )

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'
        ordering = ('-id', 'date')

    def __str__(self):
        return self.date_as_string()


class Records(models.Model):
    exercise = models.CharField('Упражнение', max_length=32)
    record = models.IntegerField('Рекорд', validators=(min_cal,))
    date = models.DateField('Дата', default=timezone.now, validators=(max_date,))

    class Meta:
        verbose_name = 'Рекорд'
        verbose_name_plural = 'Рекорды'

    def __str__(self):
        return f"{self.exercise} — {self.record}"


class User(models.Model):
    title = models.CharField('Имя', max_length=32, null=True, blank=True)
    link = models.CharField('Ссылка', max_length=512, null=True, blank=True)

    class Meta:
        verbose_name = 'Пользовательская ссылка'
        verbose_name_plural = 'Пользовательские ссылки'

    def __str__(self):
        return f'{self.title} - {self.link}'

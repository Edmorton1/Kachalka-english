from django.core.exceptions import ValidationError
from datetime import time, date, datetime

def min_cal(value: int):
    if value <= 0:
        raise ValidationError('Значение не может быть нулевым или отрицательным')

def min_time(value: time):
    if value == time(hour=0, minute=0):
        raise ValidationError('Некорректное время')
    
def max_date(value):
    if (value.year > datetime.now().year) or (value.month > datetime.now().month) or ((value.day > datetime.now().day) and (value.month == datetime.now().month)):
        raise ValidationError('Некорректная дата')
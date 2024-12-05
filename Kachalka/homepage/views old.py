from django.shortcuts import render, redirect, get_object_or_404
from .models import Statistic, Records, Types, User
from .forms import RecordsForm, StatisticForm, UserForm
from django.db.models import Avg, Count
import datetime

# Вспомогательные функции

def average_time(a):
    hours = 0
    minutes = 0
    for i in range(len(a)):
        hours += a[i]['time'].hour
        minutes += a[i]['time'].minute
    return (int(hours / len(a) * 60 + minutes / len(a))//60, int(hours / len(a) * 60 + minutes / len(a)) % 60)

def day_after(dat):
    return (datetime.datetime.now().date() - dat).days

def best_result(a):
    maximum = 0
    date = None
    time = None
    calories = 0
    for i in a:
        if i['calories'] > maximum:
            maximum = i['calories']
            date = i['date']
            time = i['time']
    days = day_after(date) if date else None
    return date, maximum, time, days

# Представления

def statis():
    """Возвращает статистические данные для главной страницы."""
    statis_list = Statistic.objects.values('date', 'calories', 'time', 'type__name', 'pk').order_by('-date')
    best = best_result(statis_list)
    count = statis_list.aggregate(Count('date'))
    average_calories = round(statis_list.aggregate(Avg('calories'))['calories__avg'])
    avg_time = average_time(statis_list.values('time'))
    types = Types.objects.all()

    return {
        'statis': statis_list,
        'best_result': best,
        'count': count,
        'average_calories': average_calories,
        'average_time': avg_time,
        'types': types,
    }

def records():
    """Возвращает данные о рекордах, включая дни с момента установления рекорда."""
    records = Records.objects.values('exercise', 'record', 'date', 'pk').order_by('-id')
    records_with_days = [
        {
            'exercise': record['exercise'],
            'record': record['record'],
            'date': record['date'],
            'days_since_record': day_after(record['date']),
            'pk': record['pk']
        }
        for record in records
    ]
    return {'records': records_with_days}

def user_values():
    return {'user_values': User.objects.all(),
            'empty': [{'num': '0'}, {'num': '1'}, {'num': '2'}, {'num': '3'}, {'num': '4'}, {'num': '5'}, {'num': '6'}, {'num': '7'}, {'num': '8'}, {'num': '9'}]}

def index(request):
    """Главное представление, объединяющее данные статистики и рекордов."""
    template = 'homepage/index.html'
    context = {**statis(), **records(), **user_values()}
    return render(request, template, context)

def radd(request, pk=None):
    if pk is not None:
        instance = get_object_or_404(Records, pk=pk)
    else:
        instance = None
    form = RecordsForm(request.POST or None, instance=instance)
    template = 'homepage/index.html'
    context = {'form': form,
            **statis(), **records(), **user_values()}
    if form.is_valid():
        form.save()
        return redirect('homepage:index')

    return render(request, template, context)

def rdelete(request, pk):
    instance = get_object_or_404(Records, pk=pk)
    instance.delete()
    return redirect('homepage:index')

def sadd(request, pk=None):
    if pk is not None:
        instance = get_object_or_404(Statistic, pk=pk)
    else:
        instance = None

    form = StatisticForm(request.POST or None, instance=instance)
    context = {'form': form,
            **statis(), **records(), **user_values()}
    
    if form.is_valid():
        form.save()
        return redirect('homepage:index')

    return render(request, 'homepage/index.html', context)

def sdelete(request, pk):
    instance = get_object_or_404(Statistic, pk=pk)
    instance.delete()
    return redirect('homepage:index')

def userhref(request, pk):
    instance = get_object_or_404(User, pk=pk)
    form = UserForm(request.POST or None, instance=instance)
    context = {'form': form,
               **statis(), **records(), **user_values()}
    if form.is_valid():
        form.save()
        return redirect('homepage:index')
    
    return render(request, 'homepage/index.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.db.models import Avg, Count
from django.views.generic import UpdateView, CreateView, TemplateView
from django.urls import reverse_lazy
from .models import *
import datetime
from django.http import Http404

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
    return {'user_values': User.objects.all()}

class IndexMixin:
    template_name = 'homepage/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statis"] = statis()['statis']
        context["best_result"] = statis()['best_result']
        context["count"] = statis()['count']
        context["average_calories"] = statis()['average_calories']
        context["average_time"] = statis()['average_time']
        context["types"] = statis()['types']
        context["records"] = records()['records']
        context["user_values"] = user_values()['user_values']
        return context

class UserInSystemMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404("Вы не авторизованы для просмотра этой страницы.")
        return super().dispatch(request, *args, **kwargs)

class IndexView(IndexMixin, TemplateView):
    pass
    
class RecordsAddEditMixin(UserInSystemMixin):
    model = Records
    fields = '__all__'
    success_url = reverse_lazy('homepage:index')

class RecordsAddView(IndexMixin, RecordsAddEditMixin, CreateView):
    pass

class RecordsEditView(IndexMixin, RecordsAddEditMixin,  UpdateView):
    pass

def rdelete(request, pk):
    if not request.user.is_authenticated:
        raise Http404("Вы не авторизованы для просмотра этой страницы.")

    instance = get_object_or_404(Records, pk=pk)
    instance.delete()
    return redirect('homepage:index')

class StatisAddEditMixin(UserInSystemMixin):
    model = Statistic
    fields = '__all__'
    success_url = reverse_lazy('homepage:index')

class StatisAdd(IndexMixin, StatisAddEditMixin, CreateView):
    pass

class StatisEdit(IndexMixin, StatisAddEditMixin, UpdateView):
    pass

def sdelete(request, pk):
    if not request.user.is_authenticated:
        raise Http404("Вы не авторизованы для просмотра этой страницы.")

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

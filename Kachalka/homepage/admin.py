from django.contrib import admin

# Register your models here.
from .models import Statistic, Types, Records, User

class StatisticAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'calories',
        'time',
        'type',
    )
    list_editable = (
        'date',
        'calories',
        'time',
        'type',
    )

class RecordsAdmin(admin.ModelAdmin):
    list_display = (
        'exercise',
        'record',
        'date',
    )
    list_editable = (
        'exercise',
        'record',
    )

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'link',
    )
    list_editable = (
        'title',
        'link',
    )

admin.site.register(User)
admin.site.register(Statistic)
admin.site.register(Types)
admin.site.register(Records)
from django.contrib import admin
from .models import Habit, DailyRecord

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'user',
        'target',
        'unit',
    ]
    list_filter = ['user']

@admin.register(DailyRecord)
class DailyRecordAdmin(admin.ModelAdmin):
    list_display = [
        'habit',
        'date',
        'amount_achieved',
    ]
    list_filter = ['date','habit']

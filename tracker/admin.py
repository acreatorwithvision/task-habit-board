from django.contrib import admin
from .models import Task,Habit,HabitLog

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display=("title","user","status","priority","due_date","created_at")
    list_filter=("status","priority","due_date","created_at")
    search_fields=("title","description","user__username")

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "frequency", "target_per_week", "created_at")
    list_filter = ("frequency", "created_at")
    search_fields = ("name", "user__username")

@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display=("habit","date")
    list_filter=("date","habit__user")
    search_fields=("habit__name","habit__user__username")
# workouts/admin.py

from django.contrib import admin
from .models import WorkoutCategory, WorkoutPlan, Workout, Exercise, WorkoutExercise

class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 1

@admin.register(WorkoutCategory)
class WorkoutCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'description']
    list_filter = ['category']
    search_fields = ['name', 'description']

@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'updated_at']
    list_filter = ['created_at', 'user']
    search_fields = ['title', 'description', 'user__username']
    date_hierarchy = 'created_at'

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'date', 'start_time', 'end_time', 'duration', 'calories_burned']
    list_filter = ['date', 'category', 'user']
    search_fields = ['user__username', 'notes']
    date_hierarchy = 'date'
    inlines = [WorkoutExerciseInline]

@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ['workout', 'exercise', 'sets', 'reps', 'weight']
    list_filter = ['workout__date', 'exercise', 'workout__user']
    search_fields = ['workout__user__username', 'exercise__name', 'notes']
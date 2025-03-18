# workouts/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser

class WorkoutCategory(models.Model):
    """WorkoutCategory"""
    name = models.CharField(_('Category name'), max_length=100)
    description = models.TextField(_('Description'), blank=True)
    
    class Meta:
        verbose_name = _('Fitness category')
        verbose_name_plural = _('Fitness category')
    
    def __str__(self):
        return self.name


class WorkoutPlan(models.Model):
    """WorkoutPlan"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='workout_plans')
    title = models.CharField(_('Plan Title'), max_length=200)
    description = models.TextField(_('Plan Description'), blank=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('WorkoutPlan')
        verbose_name_plural = _('WorkoutPlan')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Workout(models.Model):
    """Workout Record Model"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='workouts')
    category = models.ForeignKey(WorkoutCategory, on_delete=models.CASCADE, related_name='workouts')
    plan = models.ForeignKey(WorkoutPlan, on_delete=models.SET_NULL, related_name='workouts', null=True, blank=True)
    date = models.DateField(_('Date'))
    start_time = models.TimeField(_('Start Time'))
    end_time = models.TimeField(_('End Time'))
    duration = models.DurationField(_('Duration'), blank=True, null=True)
    calories_burned = models.IntegerField(_('Calories Burned'), blank=True, null=True)
    notes = models.TextField(_('Notes'), blank=True)
    
    class Meta:
        verbose_name = _('Workout Record')
        verbose_name_plural = _('Workout Record')
        ordering = ['-date', '-start_time']
    
    def __str__(self):
        return f"{self.user.username} - {self.category.name} - {self.date}"
    
    def save(self, *args, **kwargs):
        # 自动计算持续时间
        if self.start_time and self.end_time:
            import datetime
            start_dt = datetime.datetime.combine(datetime.date.today(), self.start_time)
            end_dt = datetime.datetime.combine(datetime.date.today(), self.end_time)
            if end_dt < start_dt:  # 处理跨天的情况
                end_dt = end_dt + datetime.timedelta(days=1)
            self.duration = end_dt - start_dt
        super().save(*args, **kwargs)


class Exercise(models.Model):
    """Exercise Model"""
    name = models.CharField(_('Exercise Name'), max_length=100)
    category = models.ForeignKey(WorkoutCategory, on_delete=models.CASCADE, related_name='exercises')
    description = models.TextField(_('Description'), blank=True)
    
    class Meta:
        verbose_name = _('Exercise')
        verbose_name_plural = _('Exercise')
    
    def __str__(self):
        return self.name


class WorkoutExercise(models.Model):
    """Specific exercises in workout records"""
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField(_('Sets'))
    reps = models.CharField(_('Reps Per Set'), max_length=50)  # Different reps for different sets, e.g. "12,10,8"
    weight = models.CharField(_('Weight(kg)'), max_length=50, blank=True)  # Same as above, e.g. "20,25,30"
    notes = models.TextField(_('Notes'), blank=True)
    
    class Meta:
        verbose_name = _('Exercise Record')
        verbose_name_plural = _('Exercise Record')
    
    def __str__(self):
        return f"{self.exercise.name} - {self.sets}sets"
# workouts/forms.py

from django import forms
from .models import Workout, WorkoutExercise, WorkoutPlan

class WorkoutForm(forms.ModelForm):
    """WorkoutForm"""
    class Meta:
        model = Workout
        fields = ('category', 'plan', 'date', 'start_time', 'end_time', 'calories_burned', 'notes')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class WorkoutExerciseForm(forms.ModelForm):
    """WorkoutExerciseForm"""
    class Meta:
        model = WorkoutExercise
        fields = ('exercise', 'sets', 'reps', 'weight', 'notes')


WorkoutExerciseFormSet = forms.inlineformset_factory(
    Workout, WorkoutExercise, form=WorkoutExerciseForm,
    extra=1, can_delete=True
)


class WorkoutPlanForm(forms.ModelForm):
    """WorkoutPlanForm"""
    class Meta:
        model = WorkoutPlan
        fields = ('title', 'description')
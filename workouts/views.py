# workouts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.db import transaction

from .models import Workout, WorkoutCategory, WorkoutPlan, Exercise, WorkoutExercise
from .forms import WorkoutForm, WorkoutExerciseFormSet, WorkoutPlanForm


class WorkoutListView(LoginRequiredMixin, ListView):
    model = Workout
    template_name = 'workouts/workout_list.html'
    context_object_name = 'workouts'
    paginate_by = 10
    
    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user).order_by('-date', '-start_time')


class WorkoutDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Workout
    template_name = 'workouts/workout_detail.html'
    
    def test_func(self):
        workout = self.get_object()
        return self.request.user == workout.user


@login_required
def workout_create(request):
    """创建健身记录，包含运动项目"""
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                workout = form.save(commit=False)
                workout.user = request.user
                workout.save()
                
                formset = WorkoutExerciseFormSet(request.POST, instance=workout)
                if formset.is_valid():
                    formset.save()
                    messages.success(request, 'Activity creation successful!')
                    return redirect('workout-detail', pk=workout.pk)
                else:
                    messages.error(request, 'There is an error in the exercise form, please check.')
        else:
            messages.error(request, 'There is an error in the form, please check.')
    else:
        form = WorkoutForm()
        formset = WorkoutExerciseFormSet()
    
    context = {
        'form': form,
        'formset': formset,
        'categories': WorkoutCategory.objects.all(),
    }
    return render(request, 'workouts/workout_form.html', context)


@login_required
def workout_update(request, pk):
    """workout_update"""
    workout = get_object_or_404(Workout, pk=pk)
    
    if workout.user != request.user:
        messages.error(request, 'You do not have the right to modify this record')
        return redirect('workout-list')
    
    if request.method == 'POST':
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            with transaction.atomic():
                workout = form.save()
                
                formset = WorkoutExerciseFormSet(request.POST, instance=workout)
                if formset.is_valid():
                    formset.save()
                    messages.success(request, 'Activity update successful!')
                    return redirect('workout-detail', pk=workout.pk)
                else:
                    messages.error(request, 'There is an error in the exercise form, please check.')
        else:
            messages.error(request, 'There is an error in the form, please check.')
    else:
        form = WorkoutForm(instance=workout)
        formset = WorkoutExerciseFormSet(instance=workout)
    
    context = {
        'form': form,
        'formset': formset,
        'workout': workout,
        'categories': WorkoutCategory.objects.all(),
    }
    return render(request, 'workouts/workout_form.html', context)


class WorkoutDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Workout
    template_name = 'workouts/workout_confirm_delete.html'
    success_url = reverse_lazy('workout-list')
    
    def test_func(self):
        workout = self.get_object()
        return self.request.user == workout.user


class WorkoutPlanListView(LoginRequiredMixin, ListView):
    model = WorkoutPlan
    template_name = 'workouts/plan_list.html'
    context_object_name = 'plans'
    
    def get_queryset(self):
        return WorkoutPlan.objects.filter(user=self.request.user).order_by('-created_at')


class WorkoutPlanDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = WorkoutPlan
    template_name = 'workouts/plan_detail.html'
    context_object_name = 'plan'  # 这是关键设置，确保模板中可以使用 plan 变量
    
    def test_func(self):
        plan = self.get_object()
        if plan is None:
            return False
        return self.request.user == plan.user


class WorkoutPlanCreateView(LoginRequiredMixin, CreateView):
    model = WorkoutPlan
    form_class = WorkoutPlanForm
    template_name = 'workouts/plan_form.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Fitness program created successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('plan-detail', kwargs={'pk': self.object.pk})


class WorkoutPlanUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = WorkoutPlan
    form_class = WorkoutPlanForm
    template_name = 'workouts/plan_form.html'
    
    def test_func(self):
        plan = self.get_object()
        return self.request.user == plan.user
    
    def form_valid(self, form):
        messages.success(self.request, 'The fitness program has been updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('plan-detail', kwargs={'pk': self.object.pk})


class WorkoutPlanDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = WorkoutPlan
    template_name = 'workouts/plan_confirm_delete.html'
    success_url = reverse_lazy('plan-list')
    
    def test_func(self):
        plan = self.get_object()
        return self.request.user == plan.user
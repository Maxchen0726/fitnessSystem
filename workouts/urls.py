# workouts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 健身记录
    path('', views.WorkoutListView.as_view(), name='workout-list'),
    path('<int:pk>/', views.WorkoutDetailView.as_view(), name='workout-detail'),
    path('new/', views.workout_create, name='workout-create'),
    path('<int:pk>/update/', views.workout_update, name='workout-update'),
    path('<int:pk>/delete/', views.WorkoutDeleteView.as_view(), name='workout-delete'),
    
    # 健身计划
    path('plans/', views.WorkoutPlanListView.as_view(), name='plan-list'),
    path('plans/<int:pk>/', views.WorkoutPlanDetailView.as_view(), name='plan-detail'),
    path('plans/new/', views.WorkoutPlanCreateView.as_view(), name='plan-create'),
    path('plans/<int:pk>/update/', views.WorkoutPlanUpdateView.as_view(), name='plan-update'),
    path('plans/<int:pk>/delete/', views.WorkoutPlanDeleteView.as_view(), name='plan-delete'),
]
# dashboard/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('workout-analysis/', views.workout_analysis, name='workout-analysis'),
    path('body-analysis/', views.body_analysis, name='body-analysis'),
]
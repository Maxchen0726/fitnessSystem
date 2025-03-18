# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/', views.profile, name='profile'),
    path('body-records/', views.BodyRecordListView.as_view(), name='body-records'),
    path('body-records/new/', views.BodyRecordCreateView.as_view(), name='body-record-create'),
    path('body-records/<int:pk>/update/', views.BodyRecordUpdateView.as_view(), name='body-record-update'),
    path('body-records/<int:pk>/delete/', views.BodyRecordDeleteView.as_view(), name='body-record-delete'),
]
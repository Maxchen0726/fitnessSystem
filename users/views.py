# users/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import CustomUser, UserBodyRecord
from .forms import CustomUserCreationForm, CustomUserUpdateForm, UserBodyRecordForm


class CustomLoginView(LoginView):
    template_name = 'users/login.html'


class CustomLogoutView(LogoutView):
    next_page = 'login'


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Registration Successful! Now you can log in.')
        return super().form_valid(form)


@login_required
def profile(request):
    """用户个人资料页面"""
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = CustomUserUpdateForm(instance=request.user)
    
    # 获取用户的体重记录数据用于图表显示
    body_records = UserBodyRecord.objects.filter(user=request.user).order_by('date')
    
    context = {
        'form': form,
        'body_records': body_records
    }
    return render(request, 'users/profile.html', context)


class BodyRecordListView(LoginRequiredMixin, ListView):
    model = UserBodyRecord
    template_name = 'users/body_records.html'
    context_object_name = 'records'
    paginate_by = 10
    
    def get_queryset(self):
        return UserBodyRecord.objects.filter(user=self.request.user).order_by('-date')


class BodyRecordCreateView(LoginRequiredMixin, CreateView):
    model = UserBodyRecord
    form_class = UserBodyRecordForm
    template_name = 'users/body_record_form.html'
    success_url = reverse_lazy('body-records')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BodyRecordUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserBodyRecord
    form_class = UserBodyRecordForm
    template_name = 'users/body_record_form.html'
    success_url = reverse_lazy('body-records')
    
    def test_func(self):
        record = self.get_object()
        return self.request.user == record.user


class BodyRecordDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserBodyRecord
    template_name = 'users/body_record_confirm_delete.html'
    success_url = reverse_lazy('body-records')
    
    def test_func(self):
        record = self.get_object()
        return self.request.user == record.user
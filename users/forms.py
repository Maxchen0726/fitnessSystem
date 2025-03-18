# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, UserBodyRecord

# 在 users/forms.py 中

class CustomUserCreationForm(UserCreationForm):
    """自定义用户注册表单"""
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'Select Date'
            # 移除 'type': 'date' 属性以使用 jQuery datepicker
        })
    )
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'gender', 'birth_date', 'height', 'weight')


class CustomUserUpdateForm(forms.ModelForm):
    """User Profile Update Form"""
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'Select Date'
            # 移除 'type': 'date' 属性以使用 jQuery datepicker
        })
    )
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'gender', 'birth_date', 'height', 'weight', 
                 'profile_picture', 'bio', 'target_weight')


class UserBodyRecordForm(forms.ModelForm):
    """Body Metrics Record Form"""
    class Meta:
        model = UserBodyRecord
        fields = ('date', 'weight', 'body_fat', 'chest', 'waist', 'hips', 'notes')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
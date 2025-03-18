# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserBodyRecord

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'gender', 'height', 'weight', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Fitness Information', {'fields': ('gender', 'birth_date', 'height', 'weight', 'profile_picture', 'bio', 'target_weight')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Fitness Information', {'fields': ('gender', 'birth_date', 'height', 'weight')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(UserBodyRecord)
class UserBodyRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'weight', 'body_fat']
    list_filter = ['date', 'user']
    search_fields = ['user__username']
    date_hierarchy = 'date'
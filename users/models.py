# users/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """Extended user model with fitness-related information"""
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    gender = models.CharField(_('Gender'), max_length=1, choices=GENDER_CHOICES, blank=True)
    birth_date = models.DateField(_('Birth Date'), null=True, blank=True)
    height = models.FloatField(_('Height(cm)'), null=True, blank=True)
    weight = models.FloatField(_('Weight(kg)'), null=True, blank=True)
    profile_picture = models.ImageField(_('Profile Picture'), upload_to='profile_pics', blank=True)
    bio = models.TextField(_('Bio'), blank=True)
    target_weight = models.FloatField(_('target_weight(kg)'), null=True, blank=True)
    
    def __str__(self):
        return self.username
    
    def bmi(self):
        """Calculate the BMI index"""
        if self.height and self.weight:
            height_in_meters = self.height / 100
            return round(self.weight / (height_in_meters ** 2), 2)
        return None
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('User')


class UserBodyRecord(models.Model):
    """用户身体指标记录模型"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='body_records')
    date = models.DateField(_('Record Date'))
    weight = models.FloatField(_('Weight(kg)'))
    body_fat = models.FloatField(_('Body Fat(%)'), null=True, blank=True)
    chest = models.FloatField(_('Chest(cm)'), null=True, blank=True)
    waist = models.FloatField(_('Waist(cm)'), null=True, blank=True)
    hips = models.FloatField(_('Hips(cm)'), null=True, blank=True)
    notes = models.TextField(_('Notes'), blank=True)
    
    class Meta:
        verbose_name = _('Body Metrics Record')
        verbose_name_plural = _('Body Metrics Record')
        ordering = ['-date']
        unique_together = ['user', 'date']
    
    def __str__(self):
        return f"{self.user.username}s record - {self.date}"
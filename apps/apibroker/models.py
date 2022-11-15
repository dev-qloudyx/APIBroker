from django.db import models
from apps.users.models import User


# Create your models here.


class Case(models.Model):
    customer_key = models.CharField(max_length=100, default='')
    case_number = models.CharField(max_length=100, default='')
    plate_number = models.CharField(max_length=100, default='')
    created = models.DateTimeField(auto_now_add=True)
    case_file = models.FileField(upload_to='cases', blank=True, null=True)
    owner = models.ForeignKey(User, related_name='samples', on_delete=models.CASCADE, verbose_name='Owner', blank=True, null=True)
    
    class Meta:
        ordering = ['created']
    

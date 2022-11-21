from django.db import models
from apps.users.models import User

# Create your models here.

class Case(models.Model):
    """
    Stores case entry, related to :model:`users.user`.
    """
    customer_key = models.CharField(max_length=100, default='')
    case_number = models.CharField(max_length=100, default='')
    plate_number = models.CharField(max_length=100, default='')
    created = models.DateTimeField(auto_now_add=True)
    case_file = models.FileField(upload_to='cases', blank=True, null=True)
    owner = models.ForeignKey(User, related_name='cases', on_delete=models.CASCADE,
                              verbose_name='Utilizador', blank=True, null=True)
    class Meta:
        ordering = ['created']

    def __str__(self) -> str:
        return f"{self.case_number} - {self.plate_number} - {self.customer_key}"

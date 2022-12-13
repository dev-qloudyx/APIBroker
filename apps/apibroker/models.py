from django.db import models
from apps.users.models import User
from apps.apibroker.file_validator import FileValidator

# Create your models here.
validate_file = FileValidator(max_size=1024 * 100 * 1000, 
                             content_types=('application/xml','application/json', 'text/xml'))

class Case(models.Model):
    """
    Stores case entry, related to :model:`users.user`.
    """
    client_key = models.CharField(max_length=100, default='')
    customer_key = models.CharField(max_length=100, default='')
    case_number = models.CharField(max_length=100, default='')
    plate_number = models.CharField(max_length=100, default='')
    preshared_key = models.CharField(max_length=100, default='')
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, related_name='cases', on_delete=models.CASCADE,
                              verbose_name='Utilizador', blank=True, null=True)
    binary = models.BinaryField(blank=True, null=True)
    
    class Meta:
        ordering = ['created']

    def __str__(self) -> str:
        return f"{self.case_number} - {self.plate_number} - {self.customer_key}"

class UserCase(models.Model):
    client_key = models.CharField(max_length=100, default='')
    customer_key = models.CharField(max_length=100, default='')
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE, verbose_name='Utilizador', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self) -> str:
        return f"{self.customer_key} - {self.owner}"


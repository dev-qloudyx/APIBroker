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

# class FileAttachment(models.Model):
#     """
#     Stores fileAttachment entry, related to :model:`apibroker.case`.
#     """
#     file_attachment = models.FileField(max_length=250, upload_to='cases/attachments/', blank=True, null=True)
#     filename = models.CharField(max_length=250, default='', verbose_name='Filename')
#     case = models.ForeignKey(Case, related_name='attachment', on_delete=models.CASCADE, verbose_name='Anexos', blank=True, null=True)
#     mimetype = models.CharField(max_length=100, default='', verbose_name='MimeType')
#     owner = models.ForeignKey(User, related_name='file_owner', on_delete=models.CASCADE,
#                               verbose_name='Utilizador', blank=True, null=True)
#     type = models.CharField(max_length=100, default='', verbose_name='Type')
#     doc_type = models.CharField(max_length=100, default='', verbose_name='Type')
#     binary = models.BinaryField(blank=True, null=True)
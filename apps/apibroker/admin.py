from django.contrib import admin

from apps.apibroker.models import Case, UserCase

# Register your models here.

admin.site.register(Case)
admin.site.register(UserCase)
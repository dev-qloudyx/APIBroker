from django.contrib import admin

from apps.apibroker.models import CaseInstanceManager, UserCase

# Register your models here.

admin.site.register(CaseInstanceManager)
admin.site.register(UserCase)
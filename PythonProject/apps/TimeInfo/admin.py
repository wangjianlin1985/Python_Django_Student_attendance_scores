from django.contrib import admin
from apps.TimeInfo.models import TimeInfo

# Register your models here.

admin.site.register(TimeInfo,admin.ModelAdmin)
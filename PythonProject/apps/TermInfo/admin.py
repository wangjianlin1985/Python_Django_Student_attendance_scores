from django.contrib import admin
from apps.TermInfo.models import TermInfo

# Register your models here.

admin.site.register(TermInfo,admin.ModelAdmin)
from django.contrib import admin
from apps.ClassInfo.models import ClassInfo

# Register your models here.

admin.site.register(ClassInfo,admin.ModelAdmin)
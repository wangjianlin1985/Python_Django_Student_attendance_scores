from django.contrib import admin
from apps.AttendanceState.models import AttendanceState

# Register your models here.

admin.site.register(AttendanceState,admin.ModelAdmin)
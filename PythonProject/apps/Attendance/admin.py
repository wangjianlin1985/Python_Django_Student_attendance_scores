from django.contrib import admin
from apps.Attendance.models import Attendance

# Register your models here.

admin.site.register(Attendance,admin.ModelAdmin)
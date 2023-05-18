from django.contrib import admin
from apps.Student.models import Student

# Register your models here.

admin.site.register(Student,admin.ModelAdmin)
from django.contrib import admin
from apps.Course.models import Course

# Register your models here.

admin.site.register(Course,admin.ModelAdmin)
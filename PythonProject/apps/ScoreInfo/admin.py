from django.contrib import admin
from apps.ScoreInfo.models import ScoreInfo

# Register your models here.

admin.site.register(ScoreInfo,admin.ModelAdmin)
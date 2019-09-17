from django.contrib import admin
from . import models


@admin.register(models.Method)
class MethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
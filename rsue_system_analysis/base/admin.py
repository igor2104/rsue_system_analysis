from django.contrib import admin
from . import models


@admin.register(models.Document)
class FileAdmin(admin.ModelAdmin):
    list_display = ('name', )
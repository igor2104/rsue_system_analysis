from django.contrib import admin
from . import models

class FunctionAdmin(admin.TabularInline):
    model = models.Function


class ObjectAdmin(admin.TabularInline):
    model = models.Object


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    inlines = [ObjectAdmin, FunctionAdmin]



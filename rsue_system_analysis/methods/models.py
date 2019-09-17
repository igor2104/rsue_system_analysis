from django.core.validators import  URLValidator
from django.utils.translation import gettext_lazy as _
from django.db import models

class Method(models.Model):

    name = models.CharField(max_length=100, unique=True, verbose_name=_('Название'))
    url = models.CharField(max_length=100, unique=True, verbose_name=_('Модуль метода'), help_text='Name из массива urlpatterns')
    description = models.TextField(verbose_name=_('Описание'), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Метод')
        verbose_name_plural = _('Методы')
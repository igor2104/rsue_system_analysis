from django.core.validators import FileExtensionValidator, URLValidator
from django.utils.translation import gettext_lazy as _
from django.db import models


class Document(models.Model):

    name = models.CharField(max_length=100, unique=True, verbose_name=_('Название'))
    document = models.FileField(null=True, blank=True, verbose_name=_('Документ'),
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xlsx', 'xls', 'jpg', 'png', 'jpeg'])])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Документ')
        verbose_name_plural = _('Документы')
from sys_analysis.functional_completeness import FunctionalCompleteness
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models


class Group(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='func_groups', verbose_name=_('Пользователь'))
    name = models.CharField(max_length=255, verbose_name=_('Название'))
    e_p = models.FloatField(default=1, verbose_name=_('Ep'))
    e_s = models.FloatField(default=0.1, verbose_name=_('Es'))
    e_h = models.FloatField(default=0.6, verbose_name=_('Eh'))
    e_g = models.FloatField(default=0.5, verbose_name=_('Eg'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('functional_completeness:group_detail', kwargs={'pk': self.pk})

    def get_matrix(self):

        matrix = []

        objects = self.objects_list.all()
        functions = self.functions.all().prefetch_related('objects_list')

        for o in objects:
            row = []
            for f in functions:
                if f.objects_list.filter(pk=o.pk).exists():
                    row.append(1)
                    continue
                row.append(0)
            matrix.append(row)

        return matrix

    def get_matrix_for_user(self):
        matrix = {}

        objects = self.objects_list.all().prefetch_related('functions')
        functions = self.functions.all().order_by('pk')

        for f in functions:
            row = {}
            for o in objects:
                if o.functions.filter(pk=f.pk).exists():
                    row[o] = 1
                    continue
                row[o] = 0
            matrix[f] = row

        return matrix

    def functional_completeness(self):
        if self.objects_list.count() == 0 or self.functions.count() == 0:
            return None
        return FunctionalCompleteness(self.get_matrix()).calculate(self.e_p, self.e_s, self.e_h, self.e_g)

    class Meta:
        unique_together = ('user', 'name')
        verbose_name = _('Группа')
        verbose_name_plural = _('Группы')


class Object(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Название'))
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='objects_list', verbose_name=_('Группа'))

    def __str__(self):
        return '(Q{0}) {1}'.format(self.pk, self.name)

    class Meta:
        unique_together = ('group', 'name')
        verbose_name = _('Обьект')
        verbose_name_plural = _('Обьекты')


class Function(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Название'))
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='functions', verbose_name=_('Группа'))
    objects_list = models.ManyToManyField(Object, related_name='functions', verbose_name=_('Объект'), blank = True)

    def __str__(self):
        return '(R{0}) {1}'.format(self.pk, self.name)

    class Meta:
        unique_together = ('group', 'name')
        verbose_name = _('Функция')
        verbose_name_plural = _('Функции')

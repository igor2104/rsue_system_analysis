from sys_analysis.puro import PUROMethod
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models


class Poll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls', verbose_name=_('Пользователь'))
    name = models.CharField(max_length=255, verbose_name=_('Название'))

    def get_absolute_url(self):
        return reverse('puro:poll_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('user', 'name')
        verbose_name = _('Опрос')
        verbose_name_plural = _('Опросы')


class Expert(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='experts', verbose_name=_('Опрос'))
    name = models.CharField(max_length=255, verbose_name=_('ФИО'))

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('poll', 'name')
        ordering = ('poll', 'id')
        verbose_name = _('Эксперт')
        verbose_name_plural = _('Эксперты')


class Indicator(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='indicators', verbose_name=_('Опрос'))
    name = models.CharField(max_length=255, verbose_name=_('Название'))

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('poll', 'name')
        ordering = ('poll', 'id')
        verbose_name = _('Показатель')
        verbose_name_plural = _('Показатели')


class Tour(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='tours', verbose_name=_('Опрос'))
    name = models.CharField(max_length=255, verbose_name=_('Название'))
    orders = models.ManyToManyField(Expert, through='ExpertIndicatorOrder')

    def get_orders(self):
        return self.tour_orders.all().order_by('expert', 'order', 'indicator')

    def get_experts(self):
        return self.tour_orders.distinct().select_related('expert').values('expert__id', 'expert__name').order_by('expert__id')

    def puro(self):
        indicators = Indicator.objects.filter(poll=self.poll).order_by('id').values('id')

        experts_order = self.get_orders()

        experts_indicators = []
        expert_indicator = []
        old_ex = None

        for ex in experts_order:
            if not ex.expert == old_ex:
                if expert_indicator:
                    experts_indicators.append(expert_indicator)
                old_ex = ex.expert
                expert_indicator = []

            expert_indicator.append(ex.indicator.id)

        experts_indicators.append(expert_indicator)

        return PUROMethod(
            list(indicator['id'] for indicator in indicators),
            *experts_indicators
        ).disagreement_method()

    def get_absolute_url(self):
        return reverse('puro:tour_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('poll', 'name')
        ordering = ('poll', 'name')
        verbose_name = _('Тур')
        verbose_name_plural = _('Туры')


class ExpertIndicatorOrder(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='tour_orders', verbose_name=_('Тур'))
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name='expert_orders', verbose_name=_('Эксперт'))
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, related_name='indicator_orders', verbose_name=_('Показатель'))
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = ('tour', 'expert', 'indicator')
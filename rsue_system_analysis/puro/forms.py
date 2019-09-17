from django import forms
from . import models


class PollForm(forms.ModelForm):
    class Meta:
        model = models.Poll
        fields = ['name', ]

class TourForm(forms.ModelForm):
    class Meta:
        model = models.Tour
        fields = ['name', ]


TourFormSet = forms.inlineformset_factory(
    models.Poll,
    models.Tour,
    fields=('name',),
    can_delete=True,
    extra=0
)

ExpertFormSet = forms.inlineformset_factory(
    models.Poll,
    models.Expert,
    fields=('name',),
    can_delete=True,
    extra=0
)

IndicatorFormSet = forms.inlineformset_factory(
    models.Poll,
    models.Indicator,
    fields=('name',),
    can_delete=True,
    extra=0
)

class OrderFormSet(forms.BaseInlineFormSet):
    def get_queryset(self):
        return super().get_queryset().order_by('expert', 'order', 'indicator')


ExpertIndicatorOrderFormSet = forms.inlineformset_factory(
    models.Tour,
    models.Tour.orders.through,
    fields=('order', 'expert', 'indicator'),
    widgets={
        'order': forms.HiddenInput,
        'expert': forms.HiddenInput,
        'indicator': forms.HiddenInput,
    },
    formset=OrderFormSet,
    can_delete=False,
    extra=0
)
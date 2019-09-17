from django import forms
from . import models


class GroupForm(forms.ModelForm):

    class Meta:
        model = models.Group
        fields = ['name', ]

class IndicatorsForm(forms.ModelForm):

    class Meta:
        model = models.Group
        fields = ['e_p', 'e_s', 'e_h', 'e_g']


FunctionFormSet = forms.modelformset_factory(
    models.Function,
    fields=('name',),
    can_delete=True,
    extra=0
)

ObjectFormSet = forms.modelformset_factory(
    models.Object,
    fields=('name',),
    can_delete=True,
    extra=0
)

class FunctionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.group:
            group = self.instance.group
            self.fields['objects_list'].queryset = models.Object.objects.filter(group=group)

    class Meta:
        model = models.Function
        fields = ['objects_list', ]


ObjectFunctionFormSet = forms.modelformset_factory(
    models.Function,
    form=FunctionForm,
    widgets={
        'objects_list': forms.CheckboxSelectMultiple
    },
    extra=0
)
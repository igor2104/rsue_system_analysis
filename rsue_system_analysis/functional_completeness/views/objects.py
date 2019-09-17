from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .. import models, forms
from . import base


class ObjectSave(base.BaseSave):
    formset = forms.ObjectFormSet
    relation_property = 'objects_list'
    prefix = 'object'
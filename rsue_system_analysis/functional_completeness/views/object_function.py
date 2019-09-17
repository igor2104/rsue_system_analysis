from .. import models, forms
from . import base


class ObjectFunctionSave(base.BaseSave):
    is_relation = True
    formset = forms.ObjectFunctionFormSet
    relation_property = 'functions'
    prefix = 'object_function'
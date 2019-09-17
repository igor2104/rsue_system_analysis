from .. import models, forms
from . import base


class FunctionSave(base.BaseSave):
    formset = forms.FunctionFormSet
    relation_property = 'functions'
    prefix = 'function'
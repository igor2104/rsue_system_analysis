from .. import models, forms
from . import base

class ToureBase(base.BaseInlineSave):
    redirect_name = 'puro:index'
    parameter_name = 'poll_pk'
    model = models.Poll


class TourSave(ToureBase):
    formset = forms.TourFormSet
    prefix = 'tour'


class ExpertSave(ToureBase):
    formset = forms.ExpertFormSet
    prefix = 'expert'


class IndicatorSave(ToureBase):
    formset = forms.IndicatorFormSet
    prefix = 'indicator'


class OrderSave(base.BaseInlineSave):
    def get_instance(self, request, instance_id):
        try:
            instance = self.model.objects.get(pk=instance_id, poll__user=request.user)
        except self.model.DoesNotExist:
            return redirect(self.redirect_name)

        return instance

    template_form = 'puro/inc/order_formset.html'
    redirect_name = 'puro:index'
    parameter_name = 'tour_pk'
    model = models.Tour
    formset = forms.ExpertIndicatorOrderFormSet
    prefix = 'order'
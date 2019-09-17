from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django import http

from .. import models, forms


@method_decorator(login_required, name='dispatch')
class BaseInlineSave(View):
    redirect_name = '/'
    parameter_name = None
    model = None
    template_form = 'inc/inline_formset.html'

    def get_instance(self, request, instance_id):
        try:
            instance = self.model.objects.get(pk=instance_id, user=request.user)
        except self.model.DoesNotExist:
            return redirect(self.redirect_name)

        return instance

    def validate_formset(self, formset):
        if formset.is_valid():

            elements = formset.save(commit=False)

            for obj in formset.deleted_objects:
                obj.delete()

            for element in elements:
                element.save()
            return True

        return False

    def get_data(self, formset_valid, formset=None, instance=None):
        if formset_valid:
            formset = self.get_formset(instance)

        return {
            'form_html': render_to_string(
                self.template_form,
                { 'formset': formset }
            ),
        }

    def get_formset(self, instance):
        return self.formset(
            prefix=self.prefix,
            instance=instance,
        )

    def post(self, request, *args, **kwargs):
        instance = self.get_instance(request, self.kwargs[self.parameter_name])
        formset = self.formset(request.POST, prefix=self.prefix, instance=instance)
        formset_valid = self.validate_formset(formset)

        if request.is_ajax():
            if formset_valid:
                return http.JsonResponse(self.get_data(formset_valid, instance=instance))

            return http.JsonResponse(self.get_data(formset_valid, formset=formset), status=400)

        return redirect(instance.get_absolute_url())
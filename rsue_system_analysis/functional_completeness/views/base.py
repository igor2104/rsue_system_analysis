from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django import http

from .. import models, forms


@method_decorator(login_required, name='dispatch')
class BaseGroup(View):
    model = models.Group


@method_decorator(login_required, name='dispatch')
class BaseSave(View):
    is_relation = False
    template_form = 'inc/inline_formset.html'
    template_relation = 'functional_completeness/inc/object_funtion_form.html'

    def get_group(self, request, group_id):
        try:
            group = models.Group.objects.get(pk=group_id, user=request.user)
        except models.Group.DoesNotExist:
            return redirect('functional_completeness:index')

        return group

    def validate_formset(self, formset, group):
        if formset.is_valid():
            if self.is_relation:
                formset.save()
                return True

            elements = formset.save(commit=False)

            for obj in formset.deleted_objects:
                obj.delete()

            for element in elements:
                if not element.group_id:
                    element.group = group
                element.save()
            return True

        return False

    def get_data(self, formset_valid, formset=None, group=None):
        if formset_valid:
            formset = self.get_formset(group)

            if self.is_relation:
                return {
                    'relation': render_to_string(
                        self.template_relation,
                        { 'object_function_forms': formset }
                    ),
                }

            object_function_forms = forms.ObjectFunctionFormSet(
                prefix='object_function',
                queryset=group.functions.all() if group.objects_list.count() else models.Function.objects.none()
            )

            return {
                'form_html': render_to_string(
                    self.template_form,
                    { 'formset': formset }
                ),
                'relation': render_to_string(
                    self.template_relation,
                    { 'object_function_forms': object_function_forms }
                ),
            }

        if self.is_relation:
            return {
                'relation': render_to_string(
                    self.template_relation,
                    { 'object_function_forms': formset }
                ),
            }

        return {
            'form_html': render_to_string(
                self.template_form,
                { 'formset': formset }
            ),
        }

    def get_formset(self, group):

        if self.is_relation:
            return self.formset(
                prefix=self.prefix,
                queryset=getattr(group, self.relation_property).all() if group.objects_list.count() else models.Function.objects.none()
            )

        return self.formset(
            prefix=self.prefix,
            queryset=getattr(group, self.relation_property).all()
        )

    def post(self, request, *args, **kwargs):
        formset = self.formset(request.POST, prefix=self.prefix)
        group = self.get_group(request, self.kwargs['group_pk'])
        formset_valid = self.validate_formset(formset, group)

        if request.is_ajax():
            if formset_valid:
                return http.JsonResponse(self.get_data(formset_valid, group=group))

            return http.JsonResponse(self.get_data(formset_valid, formset=formset), status=400)

        return redirect(reverse('functional_completeness:group_detail', kwargs={'pk':self.kwargs['group_pk']}))
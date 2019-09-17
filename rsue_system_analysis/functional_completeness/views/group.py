from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from django import http

from .. import models, forms
from . import base


class ListGroup(base.BaseGroup, generic.ListView):

    def get_queryset(self):
        return models.Group.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group_form'] = forms.GroupForm()

        return context


class DetailGroup(base.BaseGroup, generic.DetailView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse_lazy('functional_completeness:index')

        group = self.get_object()

        context['group_form'] = forms.GroupForm(instance=group)
        context['indicators_form'] = forms.IndicatorsForm(instance=group)
        context['function_forms'] = forms.FunctionFormSet(
            prefix='function',
            queryset=group.functions.all()
        )
        context['object_forms'] = forms.ObjectFormSet(
            prefix='object',
            queryset=group.objects_list.all()
        )
        context['object_function_forms'] = forms.ObjectFunctionFormSet(
            prefix='object_function',
            queryset=group.functions.all() if group.objects_list.count() else models.Function.objects.none()
        )

        return context


class CalculateGroup(base.BaseGroup, generic.DetailView):
    template_name = 'functional_completeness/group_calculate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse_lazy('functional_completeness:index')

        group = self.get_object()
        context['matrix'] = group.get_matrix_for_user()
        context['result'] = group.functional_completeness()

        context['js_nodes'] = group.functional_completeness()

        return context


class GroupCreate(base.BaseGroup, generic.edit.CreateView):
    fields = ['name']
    template_add = 'functional_completeness/inc/group_add_form.html'
    template_element = 'functional_completeness/inc/group_element.html'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            data = {
                'html': render_to_string(
                    self.template_add,
                    { 'group_form': form }
                )
            }
            return http.JsonResponse(data, status=400)
        else:
            return response

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'html': render_to_string(
                    self.template_element,
                    { 'group': self.object }
                )
            }
            return http.JsonResponse(data)
        else:
            return response


class GroupUpdate(base.BaseGroup, generic.edit.UpdateView):
    fields = ['name']
    template_edit = 'functional_completeness/inc/group_edit_form.html'

    #TODO: проверка на пользователя

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            data = {
                'html': render_to_string(
                    self.template_edit,
                    { 'group_form': form }
                )
            }
            return http.JsonResponse(data, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'html': render_to_string(
                    self.template_edit,
                    { 'group_form': form }
                )
            }
            return http.JsonResponse(data)
        else:
            return response


class IndicatorsUpdate(base.BaseGroup, generic.edit.UpdateView):
    fields = ['e_p', 'e_s', 'e_h', 'e_g']
    template_edit = 'functional_completeness/inc/indicator_form.html'

    #TODO: проверка на пользователя

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            data = {
                'form_html': render_to_string(
                    self.template_edit,
                    { 'indicators_form': form }
                )
            }
            return http.JsonResponse(data, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'form_html': render_to_string(
                    self.template_edit,
                    { 'indicators_form': forms.IndicatorsForm(instance=self.get_object()) }
                )
            }
            return http.JsonResponse(data)
        else:
            return response


class GroupDelete(base.BaseGroup, generic.edit.DeleteView):

    def get(self, request, *args, **kwargs):
        raise http.Http404('Page does not exist')

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            object_del = self.get_object()

            if object_del.user == request.user:
                object_del.delete()
                data = {'delete': 'success'}
                return http.JsonResponse(data)

            data = {'delete': 'error'}
            return http.JsonResponse(data, status=400)

        raise http.Http404('Page does not exist')
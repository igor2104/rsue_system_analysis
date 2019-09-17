from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from django import http

from .. import models, forms

@method_decorator(login_required, name='dispatch')
class ListPoll(generic.ListView):
    model = models.Poll

    def get_queryset(self):
        return models.Poll.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['poll_form'] = forms.PollForm()

        return context


@method_decorator(login_required, name='dispatch')
class PollCreate(generic.edit.CreateView):
    model = models.Poll
    fields = ['name']
    template_add = 'puro/inc/poll_add_form.html'
    template_element = 'puro/inc/poll_element.html'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            data = {
                'html': render_to_string(
                    self.template_add,
                    { 'poll_form': form }
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
                    { 'poll': self.object }
                )
            }
            return http.JsonResponse(data)
        else:
            return response

@method_decorator(login_required, name='dispatch')
class PollUpdate(generic.edit.UpdateView):
    model = models.Poll
    fields = ['name']
    template_edit = 'puro/inc/edit_name_form.html'

    #TODO: проверка на пользователя

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            data = {
                'html': render_to_string(
                    self.template_edit,
                    {
                        'form': form,
                        'subtitle': 'Опрос'
                    }
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
                    {
                        'form': form,
                        'subtitle': 'Опрос'
                    }
                )
            }
            return http.JsonResponse(data)
        else:
            return response


@method_decorator(login_required, name='dispatch')
class PollDelete(generic.edit.DeleteView):
    model = models.Poll

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


@method_decorator(login_required, name='dispatch')
class DetailPoll(generic.DetailView):
    model = models.Poll

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse_lazy('puro:index')

        poll = self.get_object()

        context['poll_form'] = forms.PollForm(instance=poll)

        context['tour_forms'] = forms.TourFormSet(
            prefix='tour',
            instance=poll
        )

        context['expert_forms'] = forms.ExpertFormSet(
            prefix='expert',
            instance=poll
        )

        context['indicator_forms'] = forms.IndicatorFormSet(
            prefix='indicator',
            instance=poll
        )

        return context
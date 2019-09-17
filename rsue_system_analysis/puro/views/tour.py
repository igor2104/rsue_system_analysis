from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from django import http

from .. import models, forms

@method_decorator(login_required, name='dispatch')
class DetailTour(generic.DetailView):
    model = models.Tour

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tour = self.get_object()

        context['back_url'] = reverse_lazy('puro:poll_detail', kwargs={'pk': tour.poll_id})

        context['tour_form'] = forms.TourForm(instance=tour)
        context['page_name'] = 'Опрос: {0}'.format(tour.poll.name)
        context['expert_indicator_order_form'] = forms.ExpertIndicatorOrderFormSet(
                instance=tour,
                prefix='order',
            )

        return context


@method_decorator(login_required, name='dispatch')
class TourUpdate(generic.edit.UpdateView):
    model = models.Tour
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
                        'subtitle': 'Тур'
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
                        'subtitle': 'Тур'
                    }
                )
            }
            return http.JsonResponse(data)
        else:
            return response


@method_decorator(login_required, name='dispatch')
class CalculateTour(generic.DetailView):
    model = models.Tour
    template_name = 'puro/tour_calculate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tour = self.get_object()

        result = tour.puro()

        context['canonical_matrixes'] = zip(result['canonical_matrixes'], tour.get_experts())

        context['d_matrix'] = result['d_matrix']
        context['full_d_matrix'] = result['full_d_matrix']
        context['coeff'] = result['d_matrix'].find_coeff()
        context['dz_matrix'] = result['dz_matrix']

        context['back_url'] = reverse_lazy('puro:tour_detail', kwargs={'pk': tour.pk})

        context['page_name'] = 'Тур: {0}'.format(tour.name)

        return context
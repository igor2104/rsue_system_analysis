from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import render
from methods.models import Method
from . import models


@method_decorator(login_required, name='dispatch')
class IndexView(TemplateView):
    template_name = "base/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'Методы системного анализа'
        context['list_documents'] = models.Document.objects.all()
        context['list_method'] = Method.objects.all()
        return context
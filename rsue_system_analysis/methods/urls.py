
from django.urls import path, include

urlpatterns = [
    path('puro/', include('puro.urls')),
    path('func_compl/', include('functional_completeness.urls')),
]

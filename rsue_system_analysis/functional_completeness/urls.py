from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'functional_completeness'

urlpatterns = [

    path('', views.ListGroup.as_view(), name='index'),
    path('group/detail/<int:pk>/',
        views.DetailGroup.as_view(),
        name='group_detail'
    ),
    path('calculate/<int:pk>/',
        views.CalculateGroup.as_view(),
        name='calculate'
    ),

    path('group/add/',
        views.GroupCreate.as_view(),
        name='group_add'
    ),
    path('group/edit/<int:pk>/',
        views.GroupUpdate.as_view(),
        name='group_edit'
    ),
    path('group/del/<int:pk>/',
        views.GroupDelete.as_view(),
        name='group_del'
    ),

    path('group/indicators/edit/<int:pk>/',
        views.IndicatorsUpdate.as_view(),
        name='indicators_edit'
    ),

    path('function/save/<int:group_pk>/',
        views.FunctionSave.as_view(),
        name='function_save'
    ),
    path('object/save/<int:group_pk>/',
        views.ObjectSave.as_view(),
        name='object_save'
    ),
    path('relation/save/<int:group_pk>/', views.ObjectFunctionSave.as_view(), name='object_function_save'),
]
from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'puro'

urlpatterns = [
    path('', views.ListPoll.as_view(), name='index'),
    path('poll/detail/<int:pk>/',
        views.DetailPoll.as_view(),
        name='poll_detail'
    ),

    path('poll/add/',
        views.PollCreate.as_view(),
        name='poll_add'
    ),
    path('poll/edit/<int:pk>/',
        views.PollUpdate.as_view(),
        name='poll_edit'
    ),
    path('poll/del/<int:pk>/',
        views.PollDelete.as_view(),
        name='poll_del'
    ),

    path('tour/save/<int:poll_pk>/',
        views.TourSave.as_view(),
        name='tour_save'
    ),
    path('expert/save/<int:poll_pk>/',
        views.ExpertSave.as_view(),
        name='expert_save'
    ),
    path('indicator/save/<int:poll_pk>/',
        views.IndicatorSave.as_view(),
        name='indicator_save'
    ),

    path('tour/detail/<int:pk>/',
        views.DetailTour.as_view(),
        name='tour_detail'
    ),
    path('tour/calculate/<int:pk>/',
        views.CalculateTour.as_view(),
        name='tour_calculate'
    ),
    path('tour/edit/<int:pk>/',
        views.TourUpdate.as_view(),
        name='tour_edit'
    ),

    path('order/save/<int:tour_pk>/',
        views.OrderSave.as_view(),
        name='order_save'
    ),
]

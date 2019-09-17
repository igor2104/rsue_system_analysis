from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models


@receiver(post_save, sender=models.Expert)
def post_save_expert(sender, instance, created, **kwargs):
    print(created)
    if created:
        indicators = models.Indicator.objects.filter(poll=instance.poll)
        tours = models.Tour.objects.filter(poll=instance.poll)

        for tour in tours:
            for indicator in indicators:
                instance.expert_orders.create(tour=tour, indicator=indicator, order=0)


@receiver(post_save, sender=models.Tour)
def post_save_tour(sender, instance, created, **kwargs):
    if created:
        indicators = models.Indicator.objects.filter(poll=instance.poll)
        experts = models.Expert.objects.filter(poll=instance.poll)

        for expert in experts:
            for indicator in indicators:
                instance.tour_orders.create(expert=expert, indicator=indicator, order=0)


@receiver(post_save, sender=models.Indicator)
def post_save_indicator(sender, instance, created, **kwargs):
    if created:
        tours = models.Tour.objects.filter(poll=instance.poll)
        experts = models.Expert.objects.filter(poll=instance.poll)

        for tour in tours:
            for expert in experts:
                instance.indicator_orders.create(tour=tour, expert=expert, order=0)
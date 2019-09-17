from django.apps import AppConfig


class PuroConfig(AppConfig):
    name = 'puro'

    def ready(self):
        import puro.signals
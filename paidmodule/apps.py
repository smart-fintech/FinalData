from django.apps import AppConfig


class PaidmoduleConfig(AppConfig):
    name = 'paidmodule'

    def ready(self):
        import paidmodule.signals

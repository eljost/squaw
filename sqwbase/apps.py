from django.apps import AppConfig
from django.db.models.signals import post_save

from sqwbase.signals import calculation_callback


class SqwbaseConfig(AppConfig):
    name = 'sqwbase'

    def ready(self):
        from sqwbase.models import Calculation
        post_save.connect(calculation_callback, sender=Calculation)

import logging

from django.apps import AppConfig
from django.db.models.signals import post_save


class SqwbaseConfig(AppConfig):
    name = 'sqwbase'

    def ready(self):
        try:
            from calcsyncer.main import sync_calculation
        except:
           logging.warning("Couldn't find calcsycner. Skipping registration "
                           "of post_save receiver for calculations.")
           return
        from sqwbase.signals import calculation_callback
        from sqwbase.models import Calculation
        post_save.connect(calculation_callback, sender=Calculation)

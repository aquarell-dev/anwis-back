from django.apps import AppConfig


class LeftoverConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leftover'

    def ready(self):
        from .updater import start
        start()

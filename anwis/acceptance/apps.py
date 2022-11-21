from django.apps import AppConfig


class AcceptanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'acceptance'

    def ready(self):
        from .updater import start
        start()

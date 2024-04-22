from django.apps import AppConfig


class PaperTradingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'papertradingapp'

    def ready(self):
        import papertradingapp.signals
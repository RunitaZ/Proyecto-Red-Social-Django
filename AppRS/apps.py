from django.apps import AppConfig


class ApprsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AppRS'

def ready(self):
        import AppRS.signals 
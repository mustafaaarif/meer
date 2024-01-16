from django.apps import AppConfig


class MeerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'meerapp'

default_app_config = 'meerapp.apps.MeerConfig'

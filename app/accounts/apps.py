from django.apps import AppConfig
# from accounts.recivers import *

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from accounts import recivers


from django.apps import AppConfig


class MessengerConfig(AppConfig):
    name = 'messenger'

    def ready(self):
        from .receivers import post_save_message

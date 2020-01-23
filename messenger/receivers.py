# -*- coding: utf-8 -*-

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Message


# обработчик сохранения объекта сообщения
@receiver(post_save, sender=Message)
def post_save_message(sender, instance, created, **kwargs):
    # если объект был создан
    if created:
        # указываем диалогу, в котором находится данное сообщение, что это последнее сообщение
        instance.dialog.last_message = instance
        # и обновляем данный внешний ключ чата
        instance.dialog.save(update_fields=['last_message'])

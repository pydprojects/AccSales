from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from home.models import BaseModel


class Chat(BaseModel):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, _('Dialog')),
        (CHAT, _('Chat'))
    )

    type = models.CharField(_('Тип'), max_length=1, choices=CHAT_TYPE_CHOICES, default=DIALOG)
    members = models.ManyToManyField(User, verbose_name=_("Участник"))

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('users:messenger', args=[str(self.id)])


class Message(BaseModel):
    chat = models.ForeignKey(Chat, verbose_name=_("Чат"), on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name=_("Пользователь"), on_delete=models.CASCADE)
    message = models.TextField(_("Сообщение"))
    is_read = models.BooleanField(_('Прочитано'), default=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.message

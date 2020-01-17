from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from home.models import BaseModel


class Dialog(BaseModel):
    title = models.CharField(_('Тема'), max_length=64, unique=True)
    members = models.ManyToManyField(User, verbose_name=_("Участник"))

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('messenger:messages', args=[str(self.id)])


class Message(BaseModel):
    dialog = models.ForeignKey(Dialog, verbose_name=_("Диалог"), on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name=_("Пользователь"), on_delete=models.CASCADE)
    message = models.TextField(_("Сообщение"))
    is_read = models.BooleanField(_('Прочитано'), default=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.message

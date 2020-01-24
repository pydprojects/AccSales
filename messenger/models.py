from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from base.models import BaseModel


class DialogManager(models.Manager):
    use_for_related_fields = True
    # Метод принимает пользователя, для которого должна производиться выборка
    # Если пользователь не добавлен, то будет возвращены все диалоги,
    # в которых хотя бы одно сообщение не прочитано

    def unread(self, user=None):
        qs = self.get_queryset().exclude(last_message__isnull=True).filter(last_message__is_read=False)
        return qs.exclude(last_message__author=user) if user else qs


class Dialog(BaseModel):
    title = models.CharField(_('Тема'), max_length=64, unique=True)
    members = models.ManyToManyField(User, verbose_name=_("Участник"))
    # Внешний ключ на последнее сообщение,
    # Также необходимо добавить related_name, имя через которое будет ассоциироваться выборка данного сообщения из бд
    last_message = models.ForeignKey('Message', related_name='last_message', null=True, blank=True,
                                     on_delete=models.SET_NULL)
    objects = DialogManager()

    class Meta:
        ordering = ['-updated']

    def get_absolute_url(self):
        return reverse('messenger:messages', args=[str(self.id)])


class Message(BaseModel):
    dialog = models.ForeignKey(Dialog, verbose_name=_("Диалог"), on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name=_("Пользователь"), on_delete=models.CASCADE)
    text = models.TextField(_("Сообщение"))
    is_read = models.BooleanField(_('Прочитано'), default=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('messenger:messages', args=[str(self.id)])

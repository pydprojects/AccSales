from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from django.utils.translation import gettext as _

from .models import Dialog, Message


class DialogForm(forms.Form):
    name = forms.CharField(label="Тема:", max_length=64)
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.user_from = kwargs.pop('user_from', None)
        self.user_to = kwargs.pop('user_to', None)
        super(DialogForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name'].lower()
        dialog = Dialog.objects.filter(name=name)
        if dialog.count():
            raise ValidationError(_("Диалог с таким названием уже существует."), code='invalid')
        return dialog

    def save(self, commit=True):
        name = self.cleaned_data['name'].lower()
        message = self.cleaned_data['message']
        members = (self.user_from, self.user_to)
        dialog = Dialog.objects.create(name=name)
        dialog.members.add(*members)
        Message.objects.create(dialog_id=dialog.id, author_id=members[0], message=message)


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}

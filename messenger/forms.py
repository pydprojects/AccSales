from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from django.utils.translation import gettext as _

from .models import Dialog, Message


class DialogForm(forms.Form):
    title = forms.CharField(label="Тема:", max_length=64)
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.user_from = kwargs.pop('user_from', None)
        self.user_to = kwargs.pop('user_to', None)
        super(DialogForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title'].lower()
        dialog = Dialog.objects.filter(title=title)
        if dialog.count():
            raise ValidationError("Диалог с таким названием уже существует.", code='invalid')
        return title

    def save(self, commit=True):
        title = self.cleaned_data['title'].lower()
        message = self.cleaned_data['message']
        members = (self.user_from, self.user_to)
        dialog = Dialog.objects.create(title=title)
        dialog.members.add(*members)
        Message.objects.create(dialog_id=dialog.id, author_id=members[0], message=message)


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}

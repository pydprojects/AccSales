from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

from .form import MessageForm
from .models import Chat


class DialogsView(View):

    @method_decorator(login_required)
    def get(self, request):
        chats = Chat.objects.filter(members__in=[request.user.id])
        return render(request, 'messenger/dialogs.html', {'user_profile': request.user, 'chats': chats})


class MessagesView(View):

    @method_decorator(login_required)
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.members.all():
                chat.message_set.filter(is_read=False).exclude(author=request.user).update(is_read=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None

        return render(request, 'messenger/messages.html', {'user_profile': request.user,
                                                           'chat': chat,
                                                           'form': MessageForm()
                                                           })

    @method_decorator(login_required)
    def post(self, request, chat_id):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        return redirect(reverse('messenger:messages', kwargs={'chat_id': chat_id}))


class CreateDialogView(View):

    @method_decorator(login_required)
    def get(self, request, user_id):
        chats = Chat.objects.filter(members__in=[request.user.id, user_id], type=Chat.DIALOG).annotate(
            c=Count('members')).filter(c=2)
        if chats.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
        else:
            chat = chats.first()
        return redirect(reverse('messenger:messages', kwargs={'chat_id': chat.id}))

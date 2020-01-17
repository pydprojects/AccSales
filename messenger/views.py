from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import View

from .forms import MessageForm, DialogForm
from .models import Dialog


class DialogsView(View):

    @method_decorator(login_required)
    def get(self, request):
        chats = Dialog.objects.filter(members__in=[request.user.id])
        return render(request, 'messenger/dialogs.html', {'user_profile': request.user, 'chats': chats})


class MessagesView(View):

    @method_decorator(login_required)
    def get(self, request, chat_id):
        try:
            chat = Dialog.objects.get(id=chat_id)
            if request.user in chat.members.all():
                chat.message_set.filter(is_read=False).exclude(author=request.user).update(is_read=True)
            else:
                chat = None
        except Dialog.DoesNotExist:
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
    def post(self, request, user_id):
        form = DialogForm(data=request.POST, user_from=request.user.id, user_to=user_id)
        if form.is_valid():
            form.save()
            return JsonResponse({'successful_submit': True})
        else:
            return JsonResponse({'form_errors': form.errors}, status=422)

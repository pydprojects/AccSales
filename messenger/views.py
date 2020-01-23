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
        dialogs = Dialog.objects.filter(members__in=[request.user.id])
        return render(request, 'messenger/dialogs.html', {'dialogs': dialogs})


class CreateDialogView(View):

    @method_decorator(login_required)
    def post(self, request, user_id):
        form = DialogForm(data=request.POST, user_from=request.user.id, user_to=user_id)
        if form.is_valid():
            form.save()
            return JsonResponse({'successful_submit': True})
        else:
            return JsonResponse({'form_errors': form.errors}, status=422)


class MessagesView(View):

    @method_decorator(login_required)
    def get(self, request, dialog_id):
        try:
            dialog = Dialog.objects.get(id=dialog_id)
            if request.user in dialog.members.all():
                dialog.message_set.filter(is_read=False).exclude(author=request.user).update(is_read=True)
            else:
                dialog = None
        except Dialog.DoesNotExist:
            dialog = None

        return render(request, 'messenger/messages.html', {'user_profile': request.user,
                                                           'dialog': dialog,
                                                           'form': MessageForm()
                                                           })

    @method_decorator(login_required)
    def post(self, request, dialog_id):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.dialog_id = dialog_id
            message.author = request.user
            message.save()
        return redirect(reverse('messenger:messages', kwargs={'dialog_id': dialog_id}))

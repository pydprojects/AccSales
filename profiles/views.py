from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext as _
from django.views.generic import View

from .forms import LogInForm, CustomUserCreationForm, CustomUserEditForm
from .tasks import send_email_activation
from .tokens import account_activation_token
from messenger.forms import DialogForm


class LogIn(View):

    def get(self, request):
        form = LogInForm()
        return render(request, 'profiles/login.html', {'form': form})

    def post(self, request):
        form = LogInForm(request.POST)
        if form.is_valid():
            user_activated = authenticate(username=form.cleaned_data.get('username'),
                                          password=form.cleaned_data.get('password'))
            if user_activated is None:
                messages.error(request, _("Имя пользователя или пароль неверны. Пожалуйста, попробуйте еще раз."))
                return render(request, 'profiles/login.html', {'form': form})
            elif user_activated is not None:
                login(request, user_activated)
                return redirect(request.POST.get('next', 'orders:index'))  # + or redirect('orders:index')
            elif not user_activated.is_active:
                return render(request, 'profiles/unconfirmed.html', {'user': user_activated})


class LogOut(View):

    def get(self, request):
        logout(request)
        return redirect('orders:index')


class Register(View):

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'profiles/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # Generate email confirmation
            domain = get_current_site(request).domain
            recipient_mail = form.cleaned_data.get('email')
            send_email_activation.delay(user.username, domain, recipient_mail)
            return render(request, 'profiles/unconfirmed.html', {'user': user})


class Confirm(View):
    """ Confirm token validation """
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(username=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user.username, token):
            user.is_active = True
            user.save()
            messages.success(request, _("Аккаунт успешно создан."))
            return redirect('profiles:login')
        else:
            messages.error(request, _("Некорректный ключ активации аккаунта."))
            return redirect('profiles:login')


class ResendConfirmation(View):

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except (TypeError, ValueError, User.DoesNotExist):
            messages.error(request, _("Пользователь не существует."))
            return redirect('profiles:login')
        else:
            domain = get_current_site(request).domain
            send_email_activation.delay(user.username, domain, user.email)
        return render(request, 'profiles/unconfirmed.html', {'user': user})


class Profile(View):

    def get(self, request, username):
        try:
            user_data = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, _("Данного пользователя не существует."))
            return redirect('profiles:login')
        if user_data.is_active:
            # return form for modal message window
            form = DialogForm()
            return render(request, 'profiles/profile.html', {'user_data': user_data, 'form': form})
        elif not user_data.is_active:
            messages.error(request, _("Учетная запись не активирована!"))
            return redirect('profiles:login')


class EditProfile(View):

    @method_decorator(login_required)
    def get(self, request):
        form = CustomUserEditForm(user=request.user)
        return render(request, 'profiles/edit_profile.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = CustomUserEditForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('profiles:profile', kwargs={'username': request.user}))

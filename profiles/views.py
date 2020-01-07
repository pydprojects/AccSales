from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext as _

from .form import LogInForm, CustomUserCreationForm
from .tasks import send_email_activation
from .tokens import account_activation_token


def user_login(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=form.cleaned_data.get('username'))
                user_activated = authenticate(username=form.cleaned_data.get('username'),
                                              password=form.cleaned_data.get('password'))
            except User.DoesNotExist:
                messages.error(request, _("Имя пользователя или пароль неверны. Пожалуйста, попробуйте еще раз."))
                return render(request, 'profiles/login.html', {'form': form})
            if user_activated is not None:
                login(request, user_activated)
                return redirect(request.POST.get('next', 'orders:index'))  # + or redirect('home:index')
            elif not user.is_active:
                return render(request, 'profiles/unconfirmed.html', {'user': user})
    else:
        form = LogInForm()
    return render(request, 'profiles/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home:index')


def register(request):
    if request.method == 'POST':
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
    else:
        form = CustomUserCreationForm()
    return render(request, 'profiles/register.html', {'form': form})


def confirm(request, uidb64, token):
    """ Confirm token validation """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(username=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user.username, token):
        user.is_active = True
        user.save()
        messages.success(request, _("Аккаунт успешно создан."))
        return redirect('profiles:user_login')
    else:
        messages.error(request, _("Некорректный ключ активации аккаунта."))
        return redirect('profiles:user_login')


def resend_confirmation(request, username):
    try:
        user = User.objects.get(username=username)
    except (TypeError, ValueError, User.DoesNotExist):
        messages.error(request, _("Пользователь не существует."))
        return redirect('profiles:user_login')
    else:
        domain = get_current_site(request).domain
        send_email_activation.delay(user.username, domain, user.email)
    return render(request, 'profiles/unconfirmed.html', {'user': user})

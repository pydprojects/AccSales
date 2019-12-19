from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext as _

from .form import LogInForm, CustomUserCreationForm
from .tasks import send_email
from .tokens import account_activation_token


def user_login(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            try:
                user_data = User.objects.get(username=form.cleaned_data.get('username'))
                user = authenticate(username=form.cleaned_data.get('username'),
                                    password=form.cleaned_data.get('password'))
            except User.DoesNotExist:
                messages.error(request, _("User does not exist."))
                return render(request, 'profiles/login.html', {'form': form})
            if user is not None:
                login(request, user)
                return redirect(request.POST.get('next', 'news:index'))
            elif not user_data.is_active:
                return render(request, 'profiles/unconfirmed.html', {'user_data': user_data})

    else:
        form = LogInForm()
    return render(request, 'profiles/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('news:index')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.is_active = False
            user.save()
            # Generate email confirmation
            current_site = get_current_site(request)
            text = render_to_string('profiles/confirm_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            recipient_mail = form.cleaned_data.get('email')
            # Send email
            send_email.delay(recipient_mail, text)
            form = LogInForm()
            messages.info(request, _("Email with activation account link has been sent to your email address."))
            return render(request, 'profiles/login.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'profiles/register.html', {'form': form})


def confirm(request, uidb64, token):
    """ Confirm token validation """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, _("User has been created."))
        return redirect('profiles:user_login')
    else:
        messages.error(request, _("Wrong confirmation link!"))
        return redirect('profiles:user_login')


def resend_confirmation(request, username):
    try:
        user_data = User.objects.get(username=username)
    except (TypeError, ValueError, User.DoesNotExist):
        messages.error(request, _("User does not exist."))
        return redirect('profiles:user_login')
    else:
        current_site = get_current_site(request)
        text = render_to_string('profiles/confirm_email.html', {
            'user': user_data,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user_data.pk)),
            'token': account_activation_token.make_token(user_data),
        })
        # Send email
        send_email.delay(user_data.email, text)
    return render(request, 'profiles/unconfirmed.html', {'user_data': user_data})

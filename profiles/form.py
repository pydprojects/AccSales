from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class LogInForm(forms.Form):
    username = forms.CharField(label="Имя пользователя:", min_length=4, max_length=25)
    password = forms.CharField(label="Пароль:", min_length=8, widget=forms.PasswordInput)


class CustomUserCreationForm(forms.Form):

    username = forms.CharField(label='Имя пользователя:', min_length=4, max_length=25, validators=[
        RegexValidator(regex=r'^[0-9A-Za-z-_.]+$', message="Неверный формат ввода.")],
                               help_text="Имя пользователя может состоять из був, цифр и символов ./-/_")
    email = forms.EmailField(label='Email:', help_text="my_email@example.com")
    password1 = forms.CharField(label="Пароль:", widget=forms.PasswordInput, strip=False,
                                help_text=["Пароль не должен быть слишком простым.",
                                           "Состоит как минимум из 8 символов.",
                                           "Не может состоять только из цифр."])
    password2 = forms.CharField(label="Подтверждение пароля:", widget=forms.PasswordInput, strip=False,
                                help_text="Введите пароль повторно")

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError(_("Имя пользователя уже занято."), code='invalid')
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError(_("Указанный email адресс уже используеться."), code='invalid')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 is not None and validate_password(password1) is None:
            if password1 and password2 and password1 != password2:
                raise ValidationError(_("Пароли не совпадают."), code='invalid')
        else:
            ValidationError(_(""), code='invalid')
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
        )
        return user

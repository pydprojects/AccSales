import datetime

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import resolve, reverse

from .form import LogInForm, CustomUserCreationForm
from .views import user_login, register


'''FORMS TESTS'''


class CustomUserCreationFormTests(TestCase):
    def test_user_create_form_with_correct_values(self):
        usernames = ['test', 'test.', 'test-', 'test_']
        for username in usernames:
            form_data = {'email': 'test@example.com', 'username': username,
                         'birth_date': datetime.date(1988, 1, 1),
                         'role_name': 'Administrator',
                         'password1': 'testproject', 'password2': 'testproject'}
            form = CustomUserCreationForm(data=form_data)
            self.assertTrue(form.is_valid())

    def test_user_create_form_with_invalid_username(self):
        usernames = ['tes', 'test`', 'test!', 'test@', 'test#', 'test$', 'test%', 'test^', 'test&', 'test*', 'test(',
                     'test)', 'test+', 'test=', 'test[', 'test]', 'test{', 'test}', 'test;', 'test:', 'test\'',
                     'test\"', 'test\\', 'test|', 'test/', 'test<', 'test>', 'test?']
        for username in usernames:
            form_data = {'email': 'test@example.com', 'username': username,
                         'password1': 'testproject', 'password2': 'testproject'}
            form = CustomUserCreationForm(data=form_data)
            self.assertFalse(form.is_valid())

    def test_user_create_form_with_too_short_usernmae(self):
        form_data = {'email': 'test@example.com', 'username': 'tes',
                     'password1': 'testproject', 'password2': 'testproject'}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_user_create_form_with_too_long_usernmae(self):
        form_data = {'email': 'test@example.com', 'username': 'xz'*13,
                     'password1': 'testproject', 'password2': 'testproject'}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_user_create_form_with_do_not_much_passwords(self):
        form_data = {'email': 'test@example.com', 'username': 'test',
                     'password1': 'testprojec', 'password2': 'testproject'}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_user_create_form_username_field_label(self):
        form = CustomUserCreationForm()
        self.assertEqual(form.fields['username'].label, "Username:")

    def test_user_create_form_email_field_label(self):
        form = CustomUserCreationForm()
        self.assertEqual(form.fields['email'].label, "Email:")

    def test_user_create_form_password1_field_label(self):
        form = CustomUserCreationForm()
        self.assertEqual(form.fields['password1'].label, "Password:")

    def test_user_create_form_password2_field_label(self):
        form = CustomUserCreationForm()
        self.assertEqual(form.fields['password2'].label, "Confirm Password:")

    def test_user_create_form_username_field_min_length(self):
        form = CustomUserCreationForm()
        self.assertEqual(form.fields['username'].min_length, 4)

    def test_user_create_form_username_field_max_length(self):
        form = CustomUserCreationForm()
        self.assertEqual(form.fields['username'].max_length, 25)

    def test_user_create_form_username_field_help_text(self):
        form = CustomUserCreationForm()
        self.assertEqual(form.fields['username'].help_text, "Username can consist words, digits and symbols ./-/_")

    def test_user_create_form_email_field_help_text(self):
        form = CustomUserCreationForm()
        self.assertEqual(form.fields['email'].help_text, "my_email@example.com")

    def test_user_create_form_password1_field_help_text(self):
        form = CustomUserCreationForm()
        self.assertEqual(form.fields['password1'].help_text, ["Password shouldn't be too simple.",
                                                              "Password must be at least 8 symbols.",
                                                              "Password can't be digits only"])

    def test_user_create_form_password2_field_help_text(self):
        form = CustomUserCreationForm()
        self.assertEqual(form.fields['password2'].help_text, "Re-enter password.")


class CustomLogInFormTests(TestCase):
    def test_user_login_form_with_invalid_values(self):
        form_data = {'username': 'tes', 'password': 'test123'}
        form = LogInForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_user_login_form_with_too_short_login(self):
        form_data = {'username': 'tes', 'password': 'test1234'}
        form = LogInForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_user_login_form_with_too_short_password(self):
        form_data = {'username': 'test', 'password': 'test123'}
        form = LogInForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_user_login_form_with_too_long_username(self):
        form_data = {'username': 'xz'*13, 'password': 'test1234'}
        form = LogInForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_user_login_form_username_field_label(self):
        form = LogInForm()
        self.assertEqual(form.fields['username'].label, "Username:")

    def test_user_login_form_password_field_label(self):
        form = LogInForm()
        self.assertEqual(form.fields['password'].label, "Password:")

    def test_user_login_form_username_field_min_length(self):
        form = LogInForm()
        self.assertEqual(form.fields['username'].min_length, 4)

    def test_user_login_form_password_field_min_length(self):
        form = LogInForm()
        self.assertEqual(form.fields['password'].min_length, 8)

    def test_user_login_form_username_field_max_length(self):
        form = LogInForm()
        self.assertEqual(form.fields['username'].max_length, 25)


'''VIEWS TESTS'''


class UserLogInViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test', password='test1234')
        cls.url = reverse('profiles:user_login')

    def setUp(self):
        self.response = self.client.get(self.url)
        self.response_post = self.client.post(self.url, kwargs={'username': self.user, 'password': self.user})
        self.response_post_invalid = self.client.post(self.url, {})

    def test_url_exists_at_desired_location(self):
        url = '/profile/login/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        url = reverse('profiles:user_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        url = reverse('profiles:user_login')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'profiles/login.html')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, LogInForm)

    def test_form_inputs(self):
        a = self.response
        self.assertContains(self.response, '<input', 3)

    def test_form_errors(self):
        form = self.response_post_invalid.context.get('form')
        self.assertTrue(form.errors)

    def test_csrf(self):
        url = reverse('profiles:user_login')
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_view_function(self):
        view = resolve('/profile/login/')
        self.assertEquals(view.func, user_login)

    def test_login_with_user_exists(self):
        data = {'username': 'test', 'password': 'test1234'}
        response = self.client.post(self.url, data=data)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_redirection_after_login(self):
        data = {'username': 'test', 'password': 'test1234'}
        response = self.client.post(self.url, data=data)
        self.assertRedirects(response, '/news/')

    def test_login_with_user_not_exists(self):
        data = {'username': 'ghost', 'password': 'test1234'}
        response = self.client.post('/profile/login/', data=data)
        storage = [m.message for m in get_messages(response.wsgi_request)]
        self.assertEqual(response.status_code, 200)
        self.assertEqual("User does not exist.", storage[0])

    def test_login_with_invalid_password(self):
        data = {'username': 'test', 'password': 'test4321'}
        response = self.client.post('/auth/login/', data=data)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class RegisterViewTests(TestCase):
    def setUp(self):
        url = reverse('profiles:register')
        data = {'username': 'testregister', 'email': 'testregister@example.com',
                'birth_date': datetime.date(1988, 1, 1),
                'role_name': 'Administrator',
                'password1': 'testproject', 'password2': 'testproject'}
        self.response = self.client.get(url)
        self.response_post = self.client.post(url, data)

    def test_url_exists_at_desired_location(self):
        url = '/profile/register/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'profiles/register.html')

    def test_view_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CustomUserCreationForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 7)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_view_function(self):
        view = resolve('/profile/register/')
        self.assertEquals(view.func, register)

    def test_user_registration(self):
        self.assertEqual(User.objects.count(), 1)

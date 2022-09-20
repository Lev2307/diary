from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, ButtonHolder, Field
from django.utils.translation import gettext as _
from .models import VerifyDeviceModel


class RegisterForm(UserCreationForm):
    error_messages = {
        'email_exists': _('This email is already exists.'),
        'password_mismatch': _('The two password fields didn’t match.'),
        'length_password': _('Your password should consists minimum of 8 characters')
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username', css_class='form-control mb-2'),
            Field('email', css_class='form-control mb-2'),
            Field('password1', css_class='form-control mb-2'),
            Field('password2', css_class='form-control mb-2'),
            ButtonHolder(Submit('submit', 'Submit', css_class=''))
    )
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                self.error_messages['email_exists'],
            )
        else:
            return email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': ''
        }

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username', css_class='form-control mb-2'),
            Field('password', css_class='form-control mb-2'),
            ButtonHolder(Submit('submit', 'Submit', css_class='mt-2'))
    )
    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password."
        ),
    }

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
        )
    
class VerifyDeviceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('code', css_class='form-control mb-2'),
            ButtonHolder(Submit('submit', 'Submit', css_class='mt-2'))
    )
    class Meta:
        model = VerifyDeviceModel
        fields = ['code']
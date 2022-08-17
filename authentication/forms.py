from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Button, ButtonHolder, Field
from django.utils.translation import gettext as gettext

class RegisterForm(UserCreationForm):
    error_messages = {
        'email_exists': gettext('This email is already exists.'),
        'password_mismatch': gettext('The two password fields didn’t match.'),
        'length_password': gettext('Your password should consists minimum of 8 characters')
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username', css_class='form-control mb-2'),
            Field('first_name', css_class='form-control mb-2'),
            Field('last_name', css_class='form-control mb-2'),
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
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        help_texts = {
            'username': ''
        }
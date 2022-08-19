from cProfile import label
from logging import PlaceHolder
from django import forms
from .models import DiaryModel
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Button, Field

class CreateDiaryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.error_text_inline = True
        self.helper.form_class = 'form-inline w-100'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('text', css_class='form-control mb-2 resizable', PlaceHolder='record your memories here...'),
            Field('day_of_the_week', css_class='form-select mb-2'),
            ButtonHolder(Submit('submit', 'Submit', css_class='bg-success'))
        )
    class Meta:
        model = DiaryModel
        fields = ['text', 'day_of_the_week']
        labels = {
            'day_of_the_week': 'day'
        }


class EditDiaryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.error_text_inline = True
        self.helper.form_class = 'form-inline w-100'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('text', css_class='form-control mb-2 resizable', PlaceHolder='record your memories here...'),
            Field('day_of_the_week', css_class='form-select mb-2'),
            ButtonHolder(Submit('submit', 'Submit', css_class='bg-warning border-0'))
        )
    class Meta:
        model = DiaryModel
        fields = ['text', 'day_of_the_week']
        labels = {
            'day_of_the_week': 'day'
        }
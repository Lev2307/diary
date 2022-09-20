from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LogoutView, LoginView
from .forms import RegisterForm, LoginForm, VerifyDeviceForm
from django.views.generic import UpdateView
from .models import VerifyDeviceModel
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django_user_agents.utils import get_user_agent
import random


# Create your views here.
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('login')
        
class LoginView(LoginView): 
    form_class = LoginForm
    template_name = 'auth/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def form_valid(self, form):
        os_name = self.request.user_agent.os.family
        browser = self.request.user_agent.browser.family

        if not VerifyDeviceModel.objects.filter(user=form.get_user(), os_name=os_name, browser=browser).exists():
            user = User.objects.get(username=form.get_user()) # get user by its name
            #create a verification code
            code = ''
            numbers = '0123456789'
            for _ in range(6):
                code += random.choice(numbers)
            print(code)

            # create a model where we save users browser and os
            verify = VerifyDeviceModel.objects.create(code=code, os_name=os_name, browser=browser, user=form.get_user())
            verify.save()

            #send email to user
            email = user.email
            position_of_at = email.find('@')
            email = email.lower()
            new_email =  email[0]+'*****'+email[position_of_at-1:].lower()
            email_subject = 'Please, verify your device'
            verificate_message = render_to_string('auth/email_verify/email_verification_body.html', {
                                                                                                'user': user,
                                                                                                'code': verify.code,
                                                                                                'browser': browser,
                                                                                                'os_name': os_name
                                                                                                })
            email_adress = EmailMessage(email_subject, verificate_message, to=[email])
            email_adress.content_subtype = "html"
            email_adress.send()
            messages.add_message(self.request, messages.WARNING, f"It looks like you`re trying to log in from a different location or a new device. As an added security measure, please enter the 6 digit code we sent to {new_email}")
            return HttpResponseRedirect(f'/auth/verify_acc/{verify.id}/')
        else:
            auth_login(self.request, form.get_user())
            return HttpResponseRedirect(self.get_success_url())

class LogoutView(LogoutView):
    redirect_field_name = reverse_lazy("home")
    template_name = "index.html"

class VerifyDeviceView(UpdateView):
    model = VerifyDeviceModel
    form_class = VerifyDeviceForm
    template_name = 'auth/email_verify/verify.html'
    success_url = reverse_lazy('home')

    def post(self, request, verify_id, *args, **kwargs):
        model = VerifyDeviceModel.objects.get(id=verify_id)
        form = VerifyDeviceForm(request.POST or None)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if model.code == code:
                auth_login(request, model.user)
                messages.add_message(self.request, messages.SUCCESS, f'You successfully logged in as {model.user.username}')
                return HttpResponseRedirect(self.success_url)
            else:
                messages.add_message(self.request, messages.WARNING, f'Sorry, but this code is incorrect. Please, try again.')
        return render(request, self.template_name, {'form': form}) 

    def get(self, request, verify_id, *args, **kwargs):
        model = VerifyDeviceModel.objects.get(id=verify_id)
        form = VerifyDeviceForm()
        return render(request, self.template_name, {'form': form, 'user': model.user})

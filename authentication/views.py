from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.views import LogoutView, LoginView
from .forms import RegisterForm, LoginForm, VerifyAccForm
from django.views.generic import UpdateView
from .models import VerifyAccModel
from django.contrib.auth.models import User
import random
import socket


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
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        code = ''
        numbers = '1234567890'
        for _ in range(6):
            code += random.choice(numbers)
        if not VerifyAccModel.objects.filter(ip_address=ip_address, user=form.get_user()).exists():
            verify = VerifyAccModel.objects.create(code=code, ip_address=ip_address, user=form.get_user())
            print(verify.code)
            print(verify.ip_address)
            verify.save()
            return HttpResponseRedirect(f'/auth/verify_acc/{verify.id}/')
        else:
            auth_login(self.request, form.get_user())
            return HttpResponseRedirect(self.get_success_url())

class LogoutView(LogoutView):
    redirect_field_name = reverse_lazy("home")
    template_name = "index.html"

class VerifyAccountView(UpdateView):
    model = VerifyAccModel
    form_class = VerifyAccForm
    template_name = 'auth/verify.html'
    success_url = reverse_lazy('home')

    def post(self, request, verify_id, *args, **kwargs):
        model = VerifyAccModel.objects.get(id=verify_id)
        form = VerifyAccForm(request.POST or None)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            print(code)
            if model.code == code:
                auth_login(request, model.user)
                return redirect('home')
        return render(request, self.template_name, {'form': form}) 

    def get(self, request, verify_id, *args, **kwargs):
        model = VerifyAccModel.objects.get(id=verify_id)
        print(model.user.id)
        print(model.code)
        form = VerifyAccForm()
        return render(request, self.template_name, {'form': form})

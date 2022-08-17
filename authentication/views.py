from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegisterForm

# Create your views here.
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('login')

class LoginView(LoginView):
    template_name = 'auth/login.html'
    success_url = reverse_lazy('home')

class LogoutView(LogoutView):
    redirect_field_name = reverse_lazy("home")
    template_name = "index.html"
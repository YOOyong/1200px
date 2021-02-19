from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth import login, logout, authenticate
from .models import User
from .forms import SignUpForm, LoginForm
# Create your views here.

class SignUpView(FormView):
    template_name = 'register.html'
    form_class = SignUpForm
    success_url = '/'

    def form_valid(self, form):
        user = User(
            email=form.data.get('email'),
            username = form.data.get('username')
        )
        user.set_password(form.data.get('password1'))
        user.save()
        #가입 후 로그인
        login(self.request, user)

        return super().form_valid(form)

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        email = form.data.get('email')
        password = form.data.get('password')
        user = authenticate(self.request, email=email, password=password)
        login(self.request, user)

        return super().form_valid(form)





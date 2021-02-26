from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView, DetailView, FormView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from config.views import OwnerOnlyMixin
from .models import User, Profile
from .forms import SignUpForm, LoginForm, ProfileUpdateForm
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

class ProfileView(DetailView):
    model = Profile
    template_name = "profile.html"

    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs['username']) 

class ProfileUpdateView(LoginRequiredMixin, OwnerOnlyMixin, UpdateView):
    model = Profile
    template_name = 'profile_update.html'
    success_url = '/'
    fields = ['state_message', "intro", 'profile_image']

    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs['username'])



    
    





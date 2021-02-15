from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth.hashers import check_password, make_password
from .forms import SignUpForm
from .models import Account
# Create your views here.


class SignUpView(FormView):
    template_name = 'register.html'
    form_class = SignUpForm
    success_url = '/' # 리버스로 변경하자

    def form_valid(self, form):
        print('start valid')
        account = Account(
            email = form.data.get('email'),
            password = make_password(form.data.get('password1')),
            nickname = form.data.get('nickname'),
            introduce = form.data.get('introduce')
        )
        account.save()
        print('account save')
        
        return super().form_valid(form)



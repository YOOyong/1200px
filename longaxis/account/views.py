from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth.hashers import check_password, make_password
from .models import Account
# Create your views here.




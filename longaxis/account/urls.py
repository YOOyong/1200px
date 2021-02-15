from django.urls import path
from account import views

from django.urls import path, include
from account import views

app_name = 'account'

urlpatterns = [
    path('register/', views.SignUpView.as_view()),
    path('login/', views.SignInView.as_view()),
    path('logout/', views.logout),
]
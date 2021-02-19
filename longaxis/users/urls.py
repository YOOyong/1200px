from django.urls import path
from users import views
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUpView.as_view()),
    path('login/',  views.LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]

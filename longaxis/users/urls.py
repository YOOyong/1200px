from django.urls import path
from users import views
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUpView.as_view()),
    path('login/',  views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<str:username>/feed/', views.MyFeedView.as_view(),name='feed'),
    path('<str:username>/',views.ProfileView.as_view(), name='profile'),
    path('<str:username>/update/',views.ProfileUpdateView.as_view(), name='profile_update'),
    path('<str:username>/likedphotoapi',views.liked_photo_api, name='api_liked_photo_view')
]

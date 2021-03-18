from django.contrib import admin
from django.urls import path, include
from album import views

app_name = 'album'

urlpatterns = [
    path('<str:username>/<int:pk>/', views.AlbumPhotoListView.as_view(), name='album_photo_list'),
    path('<str:username>/', views.UserAlbumListView.as_view(), name='user_album_list'),
]
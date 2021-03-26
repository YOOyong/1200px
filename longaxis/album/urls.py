from django.contrib import admin
from django.urls import path, include
from album import views

app_name = 'album'

urlpatterns = [
    path('<str:username>/<int:pk>/', views.AlbumDetailView.as_view(), name='album'),
    path('<str:username>/', views.UserAlbumListView.as_view(), name='user_album_list'),
    path('<str:username>/create/', views.craete_album, name='create_album'),
    path('<int:pk>/delete', views.delete_album, name='delete_album'),
    path('<int:pk>/rename', views.rename_album, name='rename_album')
]
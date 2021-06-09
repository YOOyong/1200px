from django.contrib import admin
from django.urls import path, include
from album import views

app_name = 'album'

urlpatterns = [
    path('useralbum/<str:username>/<int:pk>/', views.AlbumDetailView.as_view(), name='album'),
    path('useralbum/<str:username>/', views.UserAlbumListView.as_view(), name='user_album_list'),
    path('useralbum/<str:username>/create/', views.craete_album, name='create_album'),
    path('<int:pk>/delete', views.delete_album, name='delete_album'),
    path('<int:pk>/rename', views.rename_album, name='rename_album'),
    path('add_photo', views.add_photo, name='add_photo'),
    path('<int:pk>/del_photo', views.del_photo, name='del_photo'),
    path('get_album_list', views.get_album_list, name='get_album_list'),
]
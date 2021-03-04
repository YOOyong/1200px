
from django.contrib import admin
from django.urls import path, include
from gallery import views

app_name = 'gallery'

urlpatterns = [
    path('', views.GalleryView.as_view(), name='gallery'),
    path('upload/', views.PhotoUploadView.as_view()),
    path('<int:pk>/', views.PhotoDetailView.as_view(), name = 'detail'),
    path('<int:pk>/delete', views.PhotoDeleteView.as_view(), name='delete'),
    path('<int:pk>/update', views.PhotoUpdateView.as_view(), name='update'),
    path('like', views.photo_like, name='photo_like'),
    path('<int:pk>/add_comment/', views.add_comment, name='add_comment'),
    path('delete_comment/<int:pk>/', views.delete_comment, name='delete_comment'),
]
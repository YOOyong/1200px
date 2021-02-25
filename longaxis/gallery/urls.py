
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
]
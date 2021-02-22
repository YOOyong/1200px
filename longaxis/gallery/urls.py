
from django.contrib import admin
from django.urls import path, include
from gallery import views

app_name = 'gallery'

urlpatterns = [
    path('', views.GalleryView.as_view()),
]
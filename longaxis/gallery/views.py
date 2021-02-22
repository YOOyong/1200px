from django.shortcuts import render
from django.views.generic import ListView
from .models import Photo
# Create your views here.


class GalleryView(ListView):
    model = Photo
    template_name = 'gallery.html'
    context_object_name = 'photos'
    



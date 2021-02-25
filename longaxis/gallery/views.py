from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from config.views import OwnerOnlyMixin
from django.http import Http404
from .models import Photo
# Create your views here.


class GalleryView(ListView):
    model = Photo
    template_name = 'gallery.html'
    context_object_name = 'photos'
    ordering = ('-date_posted')


class PhotoUploadView(LoginRequiredMixin, CreateView):
    model = Photo
    template_name = 'upload.html'
    fields = ['image','title','description']
    success_url = '/gallery'

    def form_valid(self, form): #폼에 user 입력.
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.user = current_user
            return super(PhotoUploadView, self).form_valid(form)
        else:
            return reverse_lazy('gallery:gallery')

class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'photo_detail.html'

class PhotoDeleteView(OwnerOnlyMixin, DeleteView):
    model = Photo
    template_name = 'photo_delete.html'
    success_url = reverse_lazy('gallery:gallery')


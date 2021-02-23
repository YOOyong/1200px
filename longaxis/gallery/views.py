from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
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

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.photographer = current_user
            return super(PhotoUploadView, self).form_valid(form)
        else:
            return redirect('/')



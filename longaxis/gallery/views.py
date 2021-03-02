from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from config.views import OwnerOnlyMixin
from django.http import Http404, JsonResponse
from .models import Photo
import json
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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        object = self.get_object()
        total_likes =  object.total_likes()

        context['total_likes'] = total_likes
        return context

class PhotoDeleteView(OwnerOnlyMixin, DeleteView):
    model = Photo
    template_name = 'photo_delete.html'
    success_url = reverse_lazy('gallery:gallery')

class PhotoUpdateView(OwnerOnlyMixin, UpdateView):
    model = Photo
    template_name = 'photo_update.html'
    fields = ['image','title','description']
    success_url = reverse_lazy('gallery:gallery')

@login_required
def photo_like(request):
    if request.method == 'POST':
        user = request.user
        pk = request.POST.get('pk')
        photo = get_object_or_404(Photo, pk=pk)
        
        if photo.likes.filter(id = user.id).exists():
            #unlike
            photo.likes.remove(user)
            flag = False
        else:
            #like
            photo.likes.add(user)
            flag = True

        like_count = photo.total_likes()

        context = {
            'total_likes':like_count,
            'flag' : flag
        }
    
    return HttpResponse(json.dumps(context), content_type="application/json")

        




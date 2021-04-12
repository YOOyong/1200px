from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from config.views import OwnerOnlyMixin
from django.urls import reverse_lazy
from .models import UserAlbum
from gallery.models import Photo
from users.models import User
from .forms import AlbumForm
import json

# Create your views here.


class UserAlbumListView(LoginRequiredMixin, ListView):
    template_name = 'user_album_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['current_page_user'] = self.kwargs['username']
        context['form'] = AlbumForm()

        return context

    def get_queryset(self):
        if self.request.user.username == self.kwargs['username']:
            queryset = UserAlbum.objects.filter(
                user__username=self.kwargs['username'])
        else:
            queryset = UserAlbum.objects.filter(
                user__username=self.kwargs['username']).filter(is_private=False)

        return queryset


@login_required
def craete_album(request, username):
    if request.user.username == username:
        if request.method == 'POST':
            form = AlbumForm(request.POST)
            if form.is_valid():
                new_album = UserAlbum.objects.create(
                    user=request.user,
                    album_name=form.cleaned_data.get('album_name'),
                    is_private=form.cleaned_data.get('is_private'),
                )
                return redirect('album:user_album_list', username)
    else:
        raise PermissionError


@login_required
def delete_album(request, pk):
    album = get_object_or_404(UserAlbum, pk=pk)
    if (request.user == album.user) or request.user.is_admin:
        album.delete()
        return redirect('album:user_album_list', request.user.username)
    else:
        raise PermissionError


@login_required
def rename_album(request, pk):
    album = get_object_or_404(UserAlbum, pk=pk)
    if request.user == album.user:
        if request.method == 'POST':
            form = AlbumForm(request.POST)
            if form.is_valid():

                album.album_name = form.cleaned_data.get('album_name')
                album.is_private = form.cleaned_data.get('is_private')
                album.save()

                return redirect('album:album', username=request.user.username,pk=pk)
    else:
        raise PermissionError


class AlbumDetailView(LoginRequiredMixin, DetailView):
    template_name = 'user_album_detail.html'
    model = UserAlbum
    
    def get_context_data(self, *args, **kwargs):
        context = super(AlbumDetailView,self).get_context_data(*args, **kwargs)
        album_rename_form = AlbumForm(None, instance=context['object'])
        context['form'] = album_rename_form
        return context

    def render_to_response(self, context, **response_kwargs):
        album = context.get('object')
        if album.user == self.request.user or not album.is_private:
            return super(AlbumDetailView, self).render_to_response(context, **response_kwargs)
        else:
            raise PermissionError

@login_required
def get_album_list(request):
    if request.method == 'GET':
        user = request.user
        albums = user.albums.all()

    return JsonResponse(serializers.serialize('json', albums), status=200, safe = False, content_type="application/json")
    # return HttpResponse(json.dumps(albums), content_type="application/json")

@login_required
def add_photo(request):
    #form으로 앨범 키와 사진 키를 받아올 것.
    if request.method == 'POST':
        photo_pk = request.POST.photo_pk
        album_pk = request.POST.photo_pk

        photo = get_object_or_404(Photo, pk=photo_pk)
        album = get_object_or_404(UserAlbum, pk=album_pk)
        
        try:
            album.album_photos.add(photo)
        except:
            pass

        return HttpResponse('add done')

    return HttpResponse('wrong approch')

@login_required
def del_photo(request, pk):
    if request.method == 'POST':
        album = get_object_or_404(UserAlbum, pk=pk)
        if (request.user == album.user) or request.user.is_admin:
            photo_pk = request.POST.get('photo_pk')
            print(photo_pk)
            photo = get_object_or_404(Photo, pk=photo_pk)
            try:
                album.album_photos.remove(photo)
            except:
                pass
            
            return redirect('album:album', username=request.user.username, pk=pk)
        else:
            raise PermissionError

    return HttpResponse('wrong approch')

            
        
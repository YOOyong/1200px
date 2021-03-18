from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from config.views import OwnerOnlyMixin
from django.urls import reverse_lazy
from .models import UserAlbum
from .forms import AlbumForm

# Create your views here.

class UserAlbumListView(LoginRequiredMixin, ListView):
    template_name = 'user_album_list.html'

    def get_queryset(self):
        if self.request.user.username == self.kwargs['username']:
            queryset = UserAlbum.objects.filter(user__username=self.kwargs['username'])
        else:
            queryset = UserAlbum.objects.filter(user__username=self.kwargs['username']).filter(is_private=False)

        return queryset
    # #앨범 추가
    # def post(self, requset):
    #     if self.request.user.username == self.kwargs['username']:
    #         form = AlbumForm(request.POST)
    #         if form.is_valid():
    #             new_album = UserAlbum(
    #                 user= request.user,
    #                 album_name=form.cleaned_data.get('album_name'),
    #                 is_private=form.cleaned_data.get('is_private')
    #                 )
    #     else:
    #         raise PermissionError

class AlbumPhotoListView(LoginRequiredMixin, DetailView):
    template_name = 'user_album_detail.html'
    model = UserAlbum

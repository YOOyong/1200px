from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from config.views import OwnerOnlyMixin
from .models import Photo, Comment
from .forms import CommentForm
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
        
        context['comment_form'] = CommentForm
        context['total_likes'] = total_likes
        return context

# class PhotoDeleteView(OwnerOnlyMixin, DeleteView):
#     model = Photo
#     template_name = 'photo_delete.html'
#     success_url = reverse_lazy('gallery:gallery')

#class view는 확인 페이지가 필요함. 모달로 처리하기 위해 function 사용
@login_required
def photo_delete(request, pk):
    photo = get_object_or_404(Photo, pk=int(pk))

    if (request.user == photo.user) or request.user.is_admin:
        photo.delete()
        return redirect('gallery:gallery')
    else:
        raise PermissionError


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

@login_required
def add_comment(request, pk):
    parent_photo = get_object_or_404(Photo, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.parent_photo = parent_photo
            comment.user = request.user
            #요청이 대댓글 요청이면.
            if request.POST.get('parent_comment'):
                p_comment_pk = request.POST.get('parent_comment')
                comment.parent_comment = get_object_or_404(Comment, pk=p_comment_pk)
                
            comment.save()
            return redirect(parent_photo.get_absolute_url())
            
    return redirect(parent_photo.get_absolute_url())


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    parent_photo = comment.parent_photo

    if (request.user == comment.user) or request.user.is_admin:
        comment.delete()
        return redirect(parent_photo.get_absolute_url())
    else:
        raise PermissionError
    






from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.generic import UpdateView, DetailView, FormView, View, ListView
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from config.views import OwnerOnlyMixin
from gallery.models import Photo, LikePhoto
from .models import User, Profile
from .forms import SignUpForm, LoginForm, ProfileUpdateForm
from django.db.models import Q
# Create your views here.

class SignUpView(FormView):
    template_name = 'register.html'
    form_class = SignUpForm
    success_url = '/'

    def form_valid(self, form):
        user = User(
            email=form.data.get('email'),
            username = form.data.get('username')
        )
        user.set_password(form.data.get('password1'))
        user.save()
        #login after sign up
        login(self.request, user)

        return super().form_valid(form)

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form):
        email = form.data.get('email')
        password = form.data.get('password')
        user = authenticate(self.request, email=email, password=password)
        login(self.request, user)

        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        if next_url:
            return next_url
        else:
            return reverse('gallery:gallery')

# def LoginView(request):
#     next_page = request.GET.get('next', '/gallery')
#     # if request.user.is_authenticated:
#     #     return HttpResponseRedirect(next_page)
#     # else:
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = authenticate(request, email=email, password=password)
#             login(request, user)

#             return HttpResponseRedirect(next_page)
#         else:
#             return render(request, "login.html", {'form': form})
#     else:
#         form = LoginForm()
#         return render(request, "login.html", {'form': form})


class ProfileView(DetailView):
    model = Profile
    template_name = "profile.html"

    #url에서 받아온 username으로 object를 가져옴.
    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs['username']) 

    def get_context_data(self, *args, **kwargs):
        object = self.get_object()
        context = super().get_context_data(*args, **kwargs)

        #get total followers and following
        total_followers = object.user.total_followers()
        total_following = object.user.total_following()
        
        #is request user follow this profile user?
        is_follow = True if self.request.user.is_authenticated and self.request.user.following.filter(id = object.user.id).exists() else False
        
        #get this users photo
        photos = Photo.objects.filter(user=object.user.id)
        like_photos = LikePhoto.objects.filter(user = object.user)
        
        context['like_photos'] = like_photos
        context['total_followers'] = total_followers
        context['total_following'] = total_following
        context['is_follow'] = is_follow
        context['photos'] = photos
        
        return context

        
class ProfileUpdateView(LoginRequiredMixin, OwnerOnlyMixin, UpdateView):
    model = Profile
    template_name = 'profile_update.html'
    form_class = ProfileUpdateForm

    def get_success_url(self):
        return reverse('users:profile', args=[self.kwargs['username']])

    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs['username'])


# class FollowView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         follow_from = request.user
#         follow_to_username = request.POST.get('follow_to')
#         follow_to = get_object_or_404(User, username=follow_to_username)
    
#         try: #삭제를 일단 시도
#             follow_obj = Follow.objects.get(follow_from=follow_from, follow_to=follow_to)
#             follow_obj.delete()
#         except Follow.DoesNotExist: #없다는 에러 나면 새로 만든다.
#             follow_obj = Follow.objects.create(follow_from=follow_from, follow_to=follow_to)

#         return redirect(request.META.get('HTTP_REFERER'))

class FollowView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        follow_to_username = request.POST.get('follow_to')
        follow_to = get_object_or_404(User, username = follow_to_username)

        if request.user.following.filter(id = follow_to.id).exists():
            request.user.following.remove(follow_to)
        else:
            request.user.following.add(follow_to)

        return redirect(request.META.get('HTTP_REFERER'))


class MyFeedView(LoginRequiredMixin, ListView):
    template_name = 'feed.html'
    context_object_name = 'photos'
    
    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs['username'])
        followlist = user.following.all()
        
        return Photo.objects.filter(Q(user = user) | Q(user__in = followlist)).order_by('-date_posted')
 

# test
def liked_photo_api(request, username):
    if request.method == 'GET':
        #좋아요한 것만 가져오기
        profile_user = get_object_or_404(User, username = username)
        liked_photos = profile_user.likes.all()

        return JsonResponse(serializers.serialize('json', liked_photos), status=200, safe = False, content_type="application/json")

    




    

   


        


        

 
        


    
    





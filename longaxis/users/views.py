from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView, DetailView, FormView, View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from config.views import OwnerOnlyMixin
from .models import User, Profile
from .forms import SignUpForm, LoginForm, ProfileUpdateForm
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
        #가입 후 로그인
        login(self.request, user)

        return super().form_valid(form)

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        email = form.data.get('email')
        password = form.data.get('password')
        user = authenticate(self.request, email=email, password=password)
        login(self.request, user)

        return super().form_valid(form)

class ProfileView(DetailView):
    model = Profile
    template_name = "profile.html"

    #url에서 받아온 username으로 object를 가져옴.
    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs['username']) 

#프로필 수정
class ProfileUpdateView(LoginRequiredMixin, OwnerOnlyMixin, UpdateView):
    model = Profile
    template_name = 'profile_update.html'
    success_url = '/'
    fields = ['state_message', "intro", 'profile_image']

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

        


        

 
        


    
    





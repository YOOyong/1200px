from django import forms
from .models import User, Profile
from django.core.files import File
from PIL import Image
from django.core.files.images import get_image_dimensions

class SignUpForm(forms.ModelForm):
    email = forms.EmailField(label='이메일', error_messages={'required': '이메일을 입력하세요.'},
        max_length=100,
    )
    username = forms.CharField(label='닉네임',error_messages={'required': '닉네임을 입력하세요.'},
        max_length=20,
    )
    password1 = forms.CharField(label='비밀번호',error_messages={'required':'비밀번호를 입력하세요'},
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(label='비밀번호 확인',error_messages={'required':'비밀번호를 입력하세요'},
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('존재하는 이메일입니다')

        return email
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('존재하는 닉네임입니다')

        return username

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')

        return password2
        
class LoginForm(forms.Form):
    email  = forms.EmailField(label='이메일', error_messages={'required': '이메일을 입력하세요.'},
        max_length=100,
    )
    password = forms.CharField(label='비밀번호',error_messages={'required':'비밀번호를 입력하세요'},
        widget=forms.PasswordInput,
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    return self.cleaned_data
                else:
                    self.add_error('password', forms.ValidationError('비밀번호를 확인하세요'))
            except User.DoesNotExist:
                    self.add_error('email', forms.ValidationError('존재하지 않는 아이디입니다.'))


class ProfileUpdateForm(forms.ModelForm):

    state_message = forms.CharField(label = '상태메세지')
    intro = forms.CharField(max_length=500,label='자기소개')
    profile_image = forms.ImageField()

    def clean_profile_image(self):
        img = self.cleaned_data.get('profile_image', None)
        width, height = get_image_dimensions(self.cleaned_data.get('profile_image', None))
        if img:
            if height < 300 or width < 300:
                raise forms.ValidationError('300px X 300px 이상의 사진을 올려주세요!')
            if img.size > 1*1024*1024:
                raise forms.ValidationError('1mb 이하의 사진을 올려주세요!')
            return img
        else:
            raise forms.ValidationError('사진이 없습니다.')
        

    class Meta:
        model = Profile
        fields = ('state_message', 'intro', 'profile_image',)

    


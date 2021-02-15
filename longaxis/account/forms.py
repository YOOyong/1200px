from django import forms
from .models import Account
from django.contrib.auth.hashers import check_password, make_password

class SignUpForm(forms.Form):
    email = forms.EmailField(
        label='이메일',
        error_messages={
            'required':'이메일을 입력하세요'
        },
        max_length=64
    )

    nickname = forms.CharField(
        label='닉네임',
        error_messages={
            'required':'닉네임을 입력하세요'
        },
        max_length=20
    )

    password1 = forms.CharField(
        label='비밀번호',
        error_messages={
            'required':'비밀번호를 입력하세요'
        },
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        error_messages={
            'required':'비밀번호를 입력하세요'
        },
        widget=forms.PasswordInput,
        label='비밀번호 확인'
    )

    introduce = forms.CharField(label = '자기소개', required = False)

    def clean_email(self):
        email = self.cleaned_data['email']

        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError('존재하는 이메일입니다')

        return email


    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']

        if Account.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError('존재하는 닉네임입니다.')

        return nickname

    def clean_password2(self):
       password1 = self.cleaned_data['password1']
       password2 = self.cleaned_data['password2']
       if password1 != password2:
           raise forms.ValidationError('비밀번호와 비밀번호 확인란의 값이 일치하지 않습니다')
       return password2

class SignInForm(forms.Form):
    email = forms.EmailField(
        label='이메일',
        error_messages={
            'required':'이메일을 입력하세요'
        },
         max_length=64
    )
    password = forms.CharField(
        label='비밀번호',
        error_messages={
            'required':'비밀번호를 입력하세요'
        },
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get('email')
        password =cleaned_data.get('password')

        if email and password:
            try:
                account = Account.objects.get(email=email)
            except Account.DoesNotExist:
                self.add_error('email','존재하지 않는 메일입니다.')
                return
            
            if not check_password(password, account.password):
                self.add_error('password','비밀번호가 틀렸습니다.')

    



    









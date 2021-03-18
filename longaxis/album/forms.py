from django import forms
from .models import UserAlbum


class AlbumForm(forms.ModelForm):

    album_name = forms.CharField(max_length=50,
        error_messages={'required':'앨범 이름을 입력하세요!'}
    )
    is_private = forms.CheckboxInput()
    
    class Meta:
        model = UserAlbum
        fields = ('album_name', 'is_private')
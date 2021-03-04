from django import forms
from .models import User, Comment

class CommentForm(forms.ModelForm):

    comment_text = forms.CharField(max_length=300,
        error_messages={'required':'내용을 입력해주세요!'},
        required=True,
    )
    class Meta:
        model = Comment
        fields= ('comment_text',)
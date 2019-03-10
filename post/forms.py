from django import forms
from .models import Post, Comment
from captcha.fields import ReCaptchaField

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields =[
            'title',
            'content',
            'image',
        ]

class CommentForm(forms.ModelForm):
    capthcha = ReCaptchaField()

    class Meta:
        model = Comment
        fields = [
            'name',
            'content',
        ]
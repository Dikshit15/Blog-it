from django import forms
from .models import Post,Comment

class PostForm(forms.ModelForm):

    class Meta:
        model=Post
        fields=('title','text',)

"""class UserRegistrationForm(forms.Form):
    username=forms.CharField(
        required=True,
        label='username',
        max_length=32
    )
    email=forms.CharField(
        required=True,
        label='Email-id',
        max_length=100,
    )
    password=forms.CharField(
        required=True,
        label='Password',
        max_length=32,
        widget=forms.PasswordInput()
    )"""

class CommentForm(forms.ModelForm):

    class Meta:
        model=Comment
        fields=('author','text',)

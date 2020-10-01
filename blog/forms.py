from django import forms
from .models import Post,Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
        required=false,
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
        fields=('author','text','date')

#class SignUpForm(UserCreationForm):
#    first_name=forms.CharField(max_length=30,required=False,help_text='Optional.')
#    last_name=forms.CharField(max_length=30,required=False,help_text='Optional.')
#    email=forms.EmailField(max_length=254,help_text='Required.Inform a valid email address.')

#    class Meta:
#        model=User
#        fields=('username','first_name','last_name','email','password1','password2')

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

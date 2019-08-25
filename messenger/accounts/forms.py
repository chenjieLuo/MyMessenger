from django.contrib.auth.models import User
from django import forms
from .models import Post


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter username here'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password here'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter e-mail here'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter username here'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password here'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter e-mail here'}))


class PostForm(forms.ModelForm):
    post = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your post here.'}))

    class Meta:
        model = Post
        fields = ['post', ]




from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment
from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email"]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["text"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
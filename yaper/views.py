from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from .models import Post, Profile, Comment

def home(request):
    posts = (Post.objects
             .select_related("author__user")
             .prefetch_related("comments__author__user"))
    return render(request, "yaper/home.html", {"posts": posts})



def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def profile(request):
    posts = Post.objects.filter(author__user = request.user)
    return render(request, "yaper/profile.html", context={'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            profile = Profile.objects.get(user = request.user)
            new_post.author = profile
            new_post.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'yaper/post.html', {"form": form})

@login_required
def create_comment(request, post_id):
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            post = Post.objects.get(id=post_id)
            profile = Profile.objects.get(user=request.user)
            new_comment.post = post
            new_comment.author = profile
            new_comment.save()
            return redirect('home')

    return render(request, 'yaper/home.html', {"form": form})



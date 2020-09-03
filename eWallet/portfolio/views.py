from django.shortcuts import render
from django.http import HttpResponse

from . models import Post
# Create your views here.

def user_home(request):
    posts = Post.objects.filter(active=True, featured=True)[0:3]
    context = {'posts':posts}
    return render(request, 'portfolio/index.html', context)

def posts(request):
    posts = Post.objects.filter(active=True)

    context = {'posts':posts}
    return render(request, 'portfolio/posts.html', context)

def post(request,pk):
    post = Post.objects.get(id=pk)

    context = {'post': post}
    return render(request, 'portfolio/post.html', context)

def profile(request):
    context = {}
    return render(request, 'portfolio/profile.html', context)


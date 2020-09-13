from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from . models import Post
from .forms import PostForm

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from .filters import PostFilter
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger

# Create your views here.

def user_home(request):
    posts = Post.objects.filter(active=True, featured=True)[0:3]
    context = {'posts':posts}
    return render(request, 'portfolio/index.html', context)

def posts(request):
    posts = Post.objects.filter(active=True)
    myFilter = PostFilter(request.GET, queryset=posts)
    posts = myFilter.qs

    page = request.GET.get('page')
    paginator = Paginator(posts , 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'posts':posts, 'myFilter':myFilter}
    return render(request, 'portfolio/posts.html', context)

def post(request,slug):
    post = Post.objects.get(slug=slug)

    context = {'post': post}
    return render(request, 'portfolio/post.html', context)

def profile(request):
    context = {}
    return render(request, 'portfolio/profile.html', context)

#CRUD views
@login_required(login_url="user_home")
def createPost(request):
    form = PostForm()

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect("posts")

    context = {'form':form}
    return render(request, 'portfolio/post_form.html', context)
    

@login_required(login_url="user_home")
def updatePost(request, slug):
    post = Post.objects.get(slug=slug)
    form = PostForm(instance=post)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
        return redirect("posts")

    context = {'form':form}
    return render(request, 'portfolio/post_form.html', context)


@login_required(login_url="user_home")
def deletePost(request, slug):
    post = Post.objects.get(slug=slug)

    if request.method == "POST":
        post.delete()
        return redirect('posts')

    context={'item':post}
    return render(request, "portfolio/delete.html", context)


def sendEmail(request):

    if request.method == 'POST':

        template = render_to_string('portfolio/email_template.html', {
            'name':request.POST['name'],
            'email':request.POST['email'],
            'message':request.POST['message'],
            })

        email = EmailMessage(
            request.POST['subject'],
            template,
            settings.EMAIL_HOST_USER,
            ['djngpython@gmail.com']
            )

        email.fail_silently=False
        email.send()

    return render(request, 'portfolio/email_sent.html')
    #return HttpResponse('Email was Sent!')





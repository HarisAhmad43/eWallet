from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import PostForm

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from .filters import PostFilter
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger

from wallet.decorators import unauthenticated_user, allowed_users, admin_only
from wallet.models import *

# Create your views here.

@login_required(login_url="login")
@allowed_users(allowed_roles=['customer','admin'])
def user_home(request):

    #posts = Post.objects.filter(active=True, featured=True)[0:3]
    context = {'posts':posts}
    return render(request, 'portfolio/index.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
def post(request,slug):
    post = Post.objects.get(slug=slug)

    context = {'post': post}
    return render(request, 'portfolio/post.html', context)



#CRUD views
@login_required(login_url="login")
def createPost(request):
    form = PostForm()

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect("posts")

    context = {'form':form}
    return render(request, 'portfolio/post_form.html', context)
    

@login_required(login_url="login")
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


@login_required(login_url="login")
def deletePost(request, slug):
    post = Post.objects.get(slug=slug)

    if request.method == "POST":
        post.delete()
        return redirect('posts')

    context={'item':post}
    return render(request, "portfolio/delete.html", context)


@login_required(login_url='login')
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




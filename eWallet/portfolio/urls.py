from django.urls import path
from . import views

urlpatterns = [
    path('user_home/', views.user_home, name="user_home"),
    path('posts/', views.posts, name="posts"),
    path('post/<slug:slug>/', views.post, name="post"),



    #CRUD paths
    path('create_post/', views.createPost, name="create_post"),
    path('update_post/<slug:slug>/', views.updatePost, name="update_post"),
    path('delete_post/<slug:slug>/', views.deletePost, name="delete_post"),

    path('send_email/', views.sendEmail, name="send_email"),

]
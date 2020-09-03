from django.urls import path
from . import views

urlpatterns = [
    path('user_home/', views.user_home, name="user_home"),
    path('posts/', views.posts, name="posts"),
    path('post/<str:pk>', views.post, name="post"),
    path('profile/', views.profile, name="profile"),


]
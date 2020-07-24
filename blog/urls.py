from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # APIs to post a comment
    path('postComment', views.postComment, name='postComment'),
    path('', views.blogHome, name='blogHome'),
    # means kuch bhi koi string likhe usse blogPost main send kar do
    path('<str:slug>', views.blogPost, name='blogPost'),


]

from django.shortcuts import render
from posts.models import Post


def home(request):
    posts = Post.objects.all()
    context = {
        'title': 'Home',
        'posts': posts
    }
    return render(request, 'home/landing_page.html', context)


def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'about/about_page.html', context)
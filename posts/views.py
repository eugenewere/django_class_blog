from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    context = {
        'title': 'Home',
        'data': [1,2,3,4,5,6,7,8,9,10]
    }
    return render(request, 'home/landing_page.html', context)


def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'about/about_page.html', context)
from django.shortcuts import render, redirect
from posts.models import Post
from posts.forms import *

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


def post_details(request, post_id):
    
    post =  Post.objects.filter(id=post_id).first()
    
    context ={
        "post": post,
        "title": post.title
    }
    return render(request, 'posts/single_post.html', context)


def create_post(request):
    context = {
        'title': "Add Post"
    }
    return render(request, 'posts/add_post.html', context)


def submit_post(request):
        
    # post_title = request.POST.get('title', '')
    # subject =  request.POST.get('subject', '')
    # desc =  request.POST.get('description', '')
    # main_image =  request.FILES.get('main_image')
    
    
    
    # Post.objects.create(
    #     title=post_title,
    #     subject=subject,
    #     description=desc,
    #     main_image=main_image,
    # )  
    
    # post_object  = Post()
    # post_object.title = post_title
    # post_object.subject =  subject
    # post_object.description =  desc
    # post_object.main_image =  main_image
    # post_object.save()   
    print(request.method)
    if request.method == 'POST':
        post_form =  PostForm(request.POST)
        if post_form.is_valid():
            post_form.save()
            return redirect('posts:home_page')
        else:
            print(post_form.errors)    
            context = {
                'title': "Add Post",
                'form': post_form
            }
            return render(request, 'posts/add_post.html', context)
    return redirect('posts:create_post')
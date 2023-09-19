from django.shortcuts import render, redirect, reverse
from posts.models import Post
from posts.forms import *

def home(request):
    posts = Post.objects.order_by("-created_at")
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
    
    
    
     
    if request.method == 'POST':
        post_form =  PostForm(request.POST)
        if post_form.is_valid():
            post_form.save()
            return redirect('posts:home_page')
        else:
            context = {
                'title': "Add Post",
                'form': post_form
            }
            return render(request, 'posts/add_post.html', context)
    return redirect('posts:create_post')


def edit_post(request, post_id):
    post = Post.objects.filter(id=post_id).first()
    if post:
        context={
        'post': post,
        'title': 'Edit Post'  
        }
        return render(request, 'posts/edit_post.html', context)
    return redirect('posts:home_page')



def submit_edit_post(request, post_id):
    post = Post.objects.filter(id=post_id).first()
    if request.method == "POST":
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect(reverse('posts:post_details', kwargs={"post_id": post_id}))
        else: 
            context = {
                'title': "Edit Post",
                'form': post_form,
                'post': post
            }
            return render(request, 'posts/edit_post.html', context)
    
        # post_title = request.POST.get('title', '')
        # subject =  request.POST.get('subject', '')
        # desc =  request.POST.get('description', '')
        # main_image =  request.POST.get('main_image')

        # print(request.POST)
        # post.title =  post_title
        # post.subject = subject
        # post.description = desc
        # post.main_image = main_image
        # post.save()
        # Post.objects.filter(id=post_id).update(
        #     title=post_title,
        #     subject=subject,
        #     description=desc,
        #     main_image=main_image
        # )
        
        
        
        return redirect(reverse('posts:post_details', kwargs={"post_id": post_id}))    
    return redirect(reverse('posts:post_details', kwargs={"post_id": post_id}))
   

def delete_post(request, post_id):
    post =  Post.objects.filter(id=post_id).first()
    if post:
        post.delete()
    return redirect('posts:home_page') 
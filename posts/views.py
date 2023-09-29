from django.shortcuts import render, redirect, reverse
from posts.models import Post, Category
from posts.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required



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

@login_required
def post_details(request, post_id):
    
    post =  Post.objects.filter(id=post_id).first()
    
    context ={
        "post": post,
        "title": post.title
    }
    return render(request, 'posts/single_post.html', context)

@login_required
def create_post(request):
    categories =  Category.objects.order_by('-created_at')
    context = {
        'title': "Add Post",
        'categories': categories
    }
    return render(request, 'posts/add_post.html', context)

@login_required
def submit_post(request):
        
    post_title = request.POST.get('title', '')   
    subject =  request.POST.get('subject', '')
    desc =  request.POST.get('description', '')
    category_id =  request.POST.get('category', '')
    main_image =  request.FILES.get('main_image')
    
    if not post_title:
        messages.error(request, 'Please Add Title')
        return redirect('posts:create_post')
    if not subject:
        messages.error(request, 'Please Add Subject')
        return redirect('posts:create_post')
    if not desc:
        messages.error(request, 'Please Add Description')
        return redirect('posts:create_post')
    if not category_id:
        messages.error(request, 'Please Add Category')
        return redirect('posts:create_post')
    if not main_image:
        messages.error(request, 'Please Add Main Image')
        return redirect('posts:create_post')
    
    category = Category.objects.filter(id=category_id).first()
    if not category:
        messages.error(request, 'Category Does not Exists')
        return redirect('posts:create_post')
    
    Post.objects.create(
        title=post_title,
        subject=subject,
        description=desc,
        main_image=main_image,
        category=category,
        author=request.user
    )  
    return redirect('posts:home_page')
   


@login_required
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
    
        post_title = request.POST.get('title', '')
        subject =  request.POST.get('subject', '')
        desc =  request.POST.get('description', '')
        main_image =  request.POST.get('main_image')
        
        
        if not post_title:
            messages.error(request, 'Please Add Title')
            return redirect('posts:create_post')
        if not subject:
            messages.error(request, 'Please Add Subject')
            return redirect('posts:create_post')
        if not desc:
            messages.error(request, 'Please Add Description')
            return redirect('posts:create_post')
        if not main_image:
            messages.error(request, 'Please Add Main Image')
            return redirect('posts:create_post')
        
        Post.objects.filter(id=post_id).update(
            title=post_title,
            subject=subject,
            description=desc,
            main_image=main_image
        )
        return redirect(reverse('posts:post_details', kwargs={"post_id": post_id}))
    return redirect(reverse('posts:post_details', kwargs={"post_id": post_id}))
   

@login_required
def delete_post(request, post_id):
    post =  Post.objects.filter(id=post_id).first()
    if post:
        post.delete()
    return redirect('posts:home_page') 


def register_page(request):
    context = {
        'title': 'Register'
    }
    return render(request,'auth/register.html', context)



def login_page(request):
    context = {
        'title': 'Login'
    }
    return render(request,'auth/login.html', context)


def register_user(request):
    if request.method == "POST":
        user_form =  UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('posts:login_page')
        else: 
            context = {
                'title': 'Register',
                'form': user_form,
            }
            return render(request,'auth/register.html', context)
    return redirect('posts:register_page')

def login_user(request):
    if request.method == "POST":
        
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        
        next_stage =  request.GET.get("next", None)
        print(next_stage)
        if not username:
            messages.error(request,"Add Username.")
            return redirect('posts:login_page')
        if not password:
            messages.error(request,"Add Password.")
            return redirect('posts:login_page')    
        """        
        if intrested in using also email as a login param
        
        from django.db.models import Q
        user_ob =  User.objects.filter(Q(username=username) | Q(email=username)).first()
        user = authenticate(username=user_ob.username, password=password)
        """
        
        user = authenticate(username=username, password=password)
        if user:
            
            login(request, user)
            messages.info(request, f"You are now logged in as {username}.")



            return redirect("posts:home_page" if not next_stage else next_stage)
        else:
            messages.error(request,"Invalid username or password.")
            return redirect('posts:login_page')
    
    return redirect('posts:login_page')



def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("posts:home_page")


@login_required
def category_page(request):
    categories = Category.objects.order_by('-created_at')
    
    ctxt={
        'title': "Categories",
        'categories': categories
    }
    return render(request, 'category/category_page.html', ctxt)

def add_category(request):
    if request.method == 'POST':
        name =  request.POST.get('name')
        
        if not name:
            messages.error(request, 'Please Add Name')
            return redirect('posts:category_page')
        if Category.objects.filter(name=name).exists():
            messages.error(request, 'Category Exists')
            return redirect('posts:category_page')
        Category.objects.create(
            name=name
        )
        messages.success(request, 'Category Added Succesfully')
        
    return redirect('posts:category_page')

def edit_category(request, item_id):
    if request.method == 'POST':
        name =  request.POST.get('name')
        category = Category.objects.filter(id=item_id).first()
        if not name:
            messages.error(request, 'Please Add Name')
            return redirect('posts:category_page')
        if not category:
            messages.error(request, 'Category Not Found')
            return redirect('posts:category_page')
        if Category.objects.filter(name__iexact=name).exclude(id=item_id).exists():
            messages.error(request, 'Category Exists')
            return redirect('posts:category_page')
        Category.objects.filter(id=item_id).update(
            name=name
        )
        messages.success(request, 'Category Added Successfully')
        
    return redirect('posts:category_page')


def delete_category(request, item_id):
    category = Category.objects.filter(id=item_id).first()
    if not category:
        messages.error(request, 'Category Not Found')
        return redirect('posts:category_page')
    category.delete()
    messages.success(request, 'Category Deleted Successfully')
    return redirect('posts:category_page')
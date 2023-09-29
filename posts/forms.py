
from django import forms
from django.core.exceptions import ValidationError
from .models import Post, User
    
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate


class UserLoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", max_length=100)
    class Meta:
        model = User
        fields = ('username', 'password')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError('Username is Required')
        if not User.objects.filter(username__iexact=username).exists():
            raise ValidationError('Username Does not Exists')
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')
        if not password:
            raise ValidationError('Password is Required')
        user_obj = authenticate(username=username, password=password )
        if not user_obj:
             raise ValidationError('Credentials do not Match')
        return password
        
        
        
        

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email','first_name','last_name','username', 'password1', 'password2')
        
    def clean_username(self):
        super(UserRegistrationForm, self).clean()
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('Username already exists')
        return username
    
    def clean_email(self):
        super(UserRegistrationForm, self).clean()
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('A user has already registered using this email')
        return email
    
    def clean_password2(self):
        super(UserRegistrationForm, self).clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password1 and not password2:
            raise forms.ValidationError('Passwords and Confirm Password  are required')
        if password1 != password2:
            raise forms.ValidationError('Passwords must match')
        
        return password2


class PostForm(forms.ModelForm):

    #seller update form
    # title  =  forms.CharField(max_length=255, required=True)
    # subject = forms.CharField(max_length=255, required=True)
    # description =  forms.CharField()
    # main_image = forms.ImageField()
    
    
    class Meta:
        model = Post
        fields = ('title', 'subject', 'description', 'main_image')
    
    def clean_title(self):
        title =  self.cleaned_data['title']
        if not title:
            raise ValidationError('Please Add Title')
        return title
    
    def clean_subject(self):
        subject =  self.cleaned_data['subject']
        if not subject:
            raise ValidationError('Please Add subject')
        return subject
    
    def clean_description(self):
        description =  self.cleaned_data['description']
        if not description:
            raise ValidationError('Please Add description')
        return description
    
    def clean_main_image(self):
        main_image =  self.cleaned_data['main_image']
        if not main_image:
            raise ValidationError('Please Add main_image')
        return main_image
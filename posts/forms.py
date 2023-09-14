
from django import forms
from django.core.exceptions import ValidationError




class PostForm(forms.Form):
    title  =  forms.CharField(max_length=255, required=True)
    subject = forms.CharField(max_length=255, required=True)
    description =  forms.Textarea()
    main_image = forms.ImageField()
    
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
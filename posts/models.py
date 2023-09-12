from django.db import models


class Post(models.Model):
    title = models.CharField(null=False, max_length=255)
    subject =  models.CharField(null=True, default='No Subject', max_length=255)
    description = models.TextField(null=False)
    main_image = models.ImageField(upload_to='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'post'
    
    def __str__(self):
        return f"{self.title} {self.created_at.strftime('%d-%m-%Y')}"



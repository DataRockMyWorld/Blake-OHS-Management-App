from django.db import models
from accounts.models import CustomUser
from django.conf import settings


class Post(models.Model):
    """
    Posts on App
    """
    
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')
        
        
    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    
    title = models.CharField(max_length=100)
    body = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=(options), default='published')
    objects = models.Manager() # Default Manager
    postobjects = PostObjects() # Custom Manager
    
    def __str__(self):
        return self.title

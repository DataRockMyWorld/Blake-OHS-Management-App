from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


AUTH_PROVIDERS = {'email': 'email', 'facebook': 'facebook', 'google': 'google', 'twitter': 'twitter', 'github': 'github'}

class CustomUser(AbstractUser):
    DEPARTMENT_CHOICES = [
        ('Operations', 'Operations'),
        ('Finance', 'Finance'),
        ('Stores', 'Stores'),
        ('HSSE', 'HSSE'),
        ('MD', 'MD'),
    ]
    

    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    is_approved = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    auth_provider=models.CharField(
        choices=AUTH_PROVIDERS.items(),
        max_length=255,
        default=AUTH_PROVIDERS.get('email'),
    )
    

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

class oneTimePassword(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    
    def __str__(self):
        return f"{self.user.first_name}-passcode"
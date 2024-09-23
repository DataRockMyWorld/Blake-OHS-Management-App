from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

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
    is_manager = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

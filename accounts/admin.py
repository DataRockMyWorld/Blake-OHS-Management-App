from django.contrib import admin
from .models import CustomUser


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm 
from .models import CustomUser

class CustomUserAdmin(UserAdmin): 
    add_form = CustomUserCreationForm 
    form = CustomUserChangeForm
    model = CustomUser
    
    list_display = [
        "email",
        "id",
        "username",
        "is_staff",
        "is_active",
        "is_approved",
    ]
    
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("is_approved", "is_manager",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("is_approved", "is_manager",)}),)
    
    

admin.site.register(CustomUser, CustomUserAdmin)
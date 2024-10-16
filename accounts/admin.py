from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm 
from .models import CustomUser

class CustomUserAdmin(UserAdmin): 
    add_form = CustomUserCreationForm 
    form = CustomUserChangeForm
    model = CustomUser
    
    # Display specific fields in the admin interface
    list_display = [
        "email",
        "id",
        "is_staff",
        "is_active",
        "is_approved",
        "is_verified",
    ]

    # Redefine fieldsets to exclude 'username' and include your custom fields
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'department', 'profile_picture')
        }),
        ('Permissions', {
            'fields': ('is_approved', 'is_manager', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Social Authentication', {
            'fields': ('auth_provider',)
        }),
    )
    
    # Redefine add_fieldsets to exclude 'username' and include your custom fields
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_approved', 'is_manager')}
        ),
    )

    # Make date_joined and last_login read-only
    readonly_fields = ('last_login', 'date_joined')

    # Use email for searching and ordering
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)


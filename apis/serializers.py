# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from posts.models import Post

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'department']
        extra_kwargs = {
            'password': {'write_only': True},  # Hide password in the response
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
            department=validated_data.get('department', None),
            profile_picture=validated_data.get('profile_picture', None)
        )
        user.is_approved = False  # Default to False, admin must approve
        user.save()
        
        # Send email notification to all superusers
        self.notify_superusers(user)
        
        return user


    def notify_superusers(self, user):
        superusers = User.objects.filter(is_superuser=True)
        recipient_list = [superuser.email for superuser in superusers if superuser.email]
        
        send_mail(
            subject="New User Registration Pending Approval",
            message=f"A new user {user.first_name} {user.last_name} has registered and is pending approval.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'created_at', 'updated_at', 'status', 'author']

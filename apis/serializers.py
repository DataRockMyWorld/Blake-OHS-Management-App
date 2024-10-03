# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from posts.models import Post
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_bytes, force_str, smart_str
from django.urls import reverse
from accounts.utils import send_normal_email
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    password2 = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password2', 'department']
        extra_kwargs = {
            'password': {'write_only': True},  # Hide password in the response
        }
        
        
    def validate(self, attrs):
        """
        Validate that the two passwords match.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        """
        Create a new user with encrypted password and return it.
        """
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
        """
        Send email notification to all superusers
        """
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
    """
    Serializer for the Post model
    """
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'created_at', 'updated_at', 'status', 'author']


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField(max_length=255)
    
    class Meta:
        fields = ['email']
    def validate_email(self, value):
        email = value
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            request = self.context.get('request')
            site_domain=get_current_site(request).domain
            relative_link = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
            abslink=f"http://{site_domain}{relative_link}"
            email_body = f'Hello, \n Use the link below to reset your password  \n {abslink}'
            data = {
                'email_body': email_body,
                'to_email': user.email,
                'email_subject': 'Reset your Password'
            }
            send_normal_email(data)
        else:
            raise serializers.ValidationError('There is no user registered with this email address')
            
        return value

class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)
    uidb64 = serializers.CharField()
    token = serializers.CharField()

    class Meta:
        fields = ['new_password', 'confirm_password', 'uidb64', 'token']

    def validate(self, data):
        # Ensure that the two passwords match
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "The two password fields didn't match."})

        try:
            uid = smart_str(urlsafe_base64_decode(data['uidb64']))
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError("Invalid token or user ID.")

        if not PasswordResetTokenGenerator().check_token(user, data['token']):
            raise ValidationError("The reset link is invalid or has expired.")

        return data

    def save(self):
        uid = smart_str(urlsafe_base64_decode(self.validated_data['uidb64']))
        user = User.objects.get(id=uid)
        new_password = self.validated_data['new_password']

        # Set the new password
        user.set_password(new_password)
        user.save()

        return user

class LogOutUserSerializer(serializers.Serializer):
    """
    Serializer for logging out a user
    """
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is invalid or expired.')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


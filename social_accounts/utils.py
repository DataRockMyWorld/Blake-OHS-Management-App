from google.auth.transport import requests 
from google.oauth2 import id_token
from accounts.models import CustomUser
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class Google():
    """
    Google Social Auth Backend
    """
    def validate(access_token):
        try:
           idinfo = id_token.verify_oauth2_token(access_token, requests.Request())
           if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
               raise ValueError('Wrong issuer.')
           return idinfo
        except Exception as e:
           raise AuthenticationFailed('Invalid credentials')
       

def login_social_user(email, password):
    user = authenticate(email=email, password=settings.SOCIAL_AUTH_PASSWORD)
    if user is None:
        raise AuthenticationFailed('Invalid credentials')
    user_tokens = user.tokens()
    if user_tokens is None:
        raise AuthenticationFailed('Failed to generate tokens')
    return {
        'email':user.email,
        'full_name':user.get_full_name(),
        'access_token':str(user_tokens.get('access')),
        'refresh_token':str(user_tokens.get('refresh')),
    }
    


def register_social_user(provider, email, first_name, last_name):
    """
    Create a new user account if and only if the user can be authenticated with
    provider's account details
    """
    filtered_user_by_email = CustomUser.objects.filter(email=email)
        
    if filtered_user_by_email.exists():
        if provider == filtered_user_by_email[0].auth_provider:
            login_social_user(email, settings.SOCIAL_AUTH_PASSWORD)
        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider
        
        )
    else:
        new_user={
            'email':email,
            'first_name':first_name,
            'last_name':last_name,
            'password': settings.SOCIAL_AUTH_PASSWORD
        }
        register_user = CustomUser.objects.create_user(**new_user)
        register_user.auth_provider = provider
        register_user.is_verified = True
        register_user.save()
        login_social_user(email=register_user.email, password=settings.SOCIAL_AUTH_PASSWORD)


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
    @staticmethod
    def validate(access_token):
        try:
           idinfo = id_token.verify_oauth2_token(access_token, requests.Request())
           if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
               raise ValueError('Wrong issuer.')
           return idinfo
        except Exception as e:
           raise AuthenticationFailed('Invalid credentials')






def register_social_user(provider, email, first_name, last_name):
    """
    Create a new user account if and only if the user can be authenticated with
    provider's account details.
    """
    old_user = CustomUser.objects.filter(email=email)
    if old_user.exists():
        if provider == old_user[0].auth_provider:
            register_user = authenticate(email=email, password=settings.SOCIAL_AUTH_PASSWORD)
            return {
                'full_name': register_user.get_full_name,
                'email': register_user.email,
                'access_token': str(register_user.tokens().get('access')),
                'refresh_token': str(register_user.tokens().get('refresh'))
            }
        else:
            raise AuthenticationFailed(
                detail=f"Please continue your login with {old_user[0].auth_provider}"
            )
    else:
        # Create a new user
        new_user_data = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'password': settings.SOCIAL_AUTH_PASSWORD
        }
        user = CustomUser.objects.create_user(**new_user_data)
        user.auth_provider = provider
        user.is_verified = True
        user.save()
        # Authenticate and generate tokens for the new user
        login_user = authenticate(email=email, password=settings.SOCIAL_AUTH_PASSWORD)
        
        tokens = login_user.tokens()
        return {
            'email': login_user.email,
            'full_name': login_user.get_full_name,
            'access_token': str(tokens.get('access')),
            'refresh_token': str(tokens.get('refresh'))
        }

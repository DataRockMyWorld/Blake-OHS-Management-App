from rest_framework import serializers
from accounts.models import CustomUser
from .utils import Google, register_social_user
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

class GoogleSignInSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=255)

    def validate(self, access_token):
        google_user_data = Google.validate(access_token)
        try:
            user_id=google_user_data['sub']
         
        except:
           raise serializers.ValidationError({'detail': 'Invalid credentials'})
       
        if google_user_data['aud'] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed('Invalid credentials')
        email=google_user_data['email']
        first_name=google_user_data['given_name']
        last_name=google_user_data['family_name']
        provider='google'

        return register_social_user(provider, email, first_name, last_name)

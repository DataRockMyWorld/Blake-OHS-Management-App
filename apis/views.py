# accounts/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from posts.models import Post
from .serializers import (
    PostSerializer, 
    UserRegistrationSerializer, 
    PasswordResetRequestSerializer, 
    SetNewPasswordSerializer,
    LogOutUserSerializer
)
from accounts.utils import send_otp_to_user
from accounts.models import oneTimePassword
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import AuthenticationFailed


User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            # send email of otp to user after registration
            send_otp_to_user(user['email'])

            return Response(
                {"message": "User registered successfully. Awaiting admin approval."}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyUserEmail(generics.GenericAPIView):
    """
    Verify user email
    """
    def post(self, request):
        otpcode = request.data.get('otp_code')
        try:
            user_code_obj = oneTimePassword.objects.get(code=otpcode)
            user = user_code_obj.user
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({"message": "User verified successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User already verified."}, status=status.HTTP_400_BAD_REQUEST)
        
        except oneTimePassword.DoesNotExist:
            return Response({"message": "Invalid OTP code."}, status=status.HTTP_400_BAD_REQUEST)



class PostList(generics.ListCreateAPIView):
    """
    List all posts, or create a new post.
    """
    queryset = Post.postobjects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a post.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminUser]

class TestAuthenticationView(generics.GenericAPIView):
    """
    Test authentication
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'msg': 'Authenticated'
        }
        return Response(content, status=status.HTTP_200_OK)

class PasswordResetRequestView(generics.GenericAPIView):
    """
    Password reset
    """
    serializer_class = PasswordResetRequestSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({"message": "A link has been sent to your email to reset your password."}, status=status.HTTP_200_OK)
    

class PasswordResetConfirm(generics.GenericAPIView):
    """
    Password reset confirm
    """
    def get(self, request, uidb64, token):
        try:
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except DjangoUnicodeDecodeError:
            return Response({"message": "Invalid token or expired."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"message": "Invalid token or expired."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success":True, "message": "Token is valid", "uidb64": uidb64, "token": token}, status=status.HTTP_200_OK)


class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Password reset successful."},
            status=status.HTTP_200_OK
        )

class LogOutUserView(generics.GenericAPIView):
    """
    Log out user
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LogOutUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User logged out successfully."}, status=status.HTTP_204_NO_CONTENT)

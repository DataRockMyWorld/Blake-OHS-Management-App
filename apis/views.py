# accounts/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from posts.models import Post
from .serializers import PostSerializer, UserRegistrationSerializer

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # Allow any user to access this view

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {"message": "User registered successfully. Awaiting admin approval."}, 
            status=status.HTTP_201_CREATED
        )

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

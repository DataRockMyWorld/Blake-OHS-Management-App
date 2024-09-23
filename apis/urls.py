# accounts/urls.py
from django.urls import path
from .views import PostList, PostDetail, UserRegistrationView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Registration
    path("register/", UserRegistrationView.as_view(), name="create_user"),
    
   # Posts
    path('posts/', PostList.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),

]

from django.urls import path
from .views import (
    PostList, 
    PostDetail, 
    UserRegistrationView, 
    VerifyUserEmail,
    SetNewPasswordView,
    PasswordResetRequestView,
    PasswordResetConfirm,
    LogOutUserView,
    CustomTokenObtainPairView,
    TestAuthenticationView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Registration
    path("register/", UserRegistrationView.as_view(), name="create_user"),
    path("verify-email/", VerifyUserEmail.as_view(), name="verify_email"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password_reset"),
    path("password-reset-confirm/<str:uidb64>/<str:token>/", PasswordResetConfirm.as_view(), name="password_reset_confirm"),
    path("set-new-password/", SetNewPasswordView.as_view(), name="set_new_password"),
    path("logout/", LogOutUserView.as_view(), name="logout"),
    
   # Posts
    path('posts/', PostList.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('test-authentication/', TestAuthenticationView.as_view(), name='test_authentication'),
]

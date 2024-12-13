from django.urls import path
from .views import (
    UserRegistrationView, 
    EmailVerificationView,
    PasswordResetRequestView, 
    PasswordResetConfirmView,
    PasswordResetCheckView,
    LoginView,
    LogoutView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # ورورد 
    path('login/', LoginView.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    
    # ثبت نام
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    
    # تایید ایمیل
    path('verify-email/<str:token>/', EmailVerificationView.as_view(), name='email-verification'),
    
    # احراز هویت (توکن)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # بازیابی رمز عبور
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/<str:token>/', PasswordResetCheckView.as_view(), name='password_reset_check'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
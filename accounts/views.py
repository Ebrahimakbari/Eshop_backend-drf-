from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.utils import timezone
from .serializers import (
    UserRegistrationSerializer, 
    PasswordResetRequestSerializer, 
    PasswordResetConfirmSerializer,
    LoginSerializer,
    UserLoginResponseSerializer
)


User = get_user_model()



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            # آماده‌سازی اطلاعات پاسخ
            response_data = {
                'user_id': serializer.validated_data['user'].id,
                'username': serializer.validated_data['user'].username,
                'email': serializer.validated_data['user'].email,
                'access_token': serializer.validated_data['access'],
                'refresh_token': serializer.validated_data['refresh']
            }
            
            # سریالایز کردن پاسخ
            response_serializer = UserLoginResponseSerializer(data=response_data)
            response_serializer.is_valid(raise_exception=True)
            
            return Response(
                response_serializer.data, 
                status=status.HTTP_200_OK
            )
        
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )


class LogoutView(APIView):
    def post(self, request):
        try:
            # دریافت توکن ریفرش از هدر درخواست
            refresh_token = request.data.get('refresh_token')
            
            # blacklist کردن توکن
            from rest_framework_simplejwt.tokens import RefreshToken
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({
                'message': 'با موفقیت خارج شدید'
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error': 'خطا در خروج'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data,
                                                context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'کاربر با موفقیت ثبت نام شد. لطفاً ایمیل خود را تایید کنید.',
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            user = User.objects.get(
                email_verification_token=token,
                is_active=False,
                token_created_at__gt=timezone.now() - timezone.timedelta(days=1)
            )
            user.is_active = True
            user.email_verification_token = None
            user.save()
            return Response({
                'message': 'ایمیل با موفقیت تایید شد'
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'error': 'توکن نامعتبر یا منقضی شده است'
            }, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data,
                                                    context={'request': request})
        if serializer.is_valid():
            email = serializer.validated_data['email']
            serializer.send_password_reset_email(email)
            return Response({
                'message': 'لینک بازیابی رمز عبور ارسال شد'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetCheckView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, token):
        try:
            user = User.objects.get(
                token=token,
                token_created_at__gt=timezone.now() - timezone.timedelta(hours=1)
            )
            return Response({
                'message': 'توکن معتبر است',
                'email': user.email,
                'token': token
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'error': 'توکن نامعتبر یا منقضی شده است'
            }, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'رمز عبور با موفقیت تغییر یافت'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
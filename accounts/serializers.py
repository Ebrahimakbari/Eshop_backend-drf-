from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .authentications import AuthenticationBackend
from rest_framework_simplejwt.tokens import RefreshToken
import uuid

User = get_user_model()



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        if email and password:
            user = AuthenticationBackend.authenticate(
                email=email, 
                password=password
            )

            if not user:
                raise serializers.ValidationError('اطلاعات ورود نادرست است')
            
            if not user.is_active:
                raise serializers.ValidationError('حساب کاربری شما فعال نیست')

            refresh = RefreshToken.for_user(user)
            
            attrs['user'] = user
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)
        
        return attrs


class UserLoginResponseSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 
            'confirm_password', 'first_name', 'last_name'
        ]
        extra_kwargs = {
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('confirm_password'):
            raise serializers.ValidationError({"password": "رمزهای عبور مطابقت ندارند"})
        
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "این ایمیل قبلاً ثبت شده است"})
        
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "این نام کاربری قبلاً انتخاب شده است"})
        
        return attrs

    def create(self, validated_data):
        email_verification_token = str(uuid.uuid4())
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email_verification_token=email_verification_token,
            token_created_at=timezone.now()
        )
        
        try:
            request = self.context.get('request')
            verification_link = f"http://{request.get_host()}/accounts/verify-email/{email_verification_token}/"
            send_mail(
                'تایید ایمیل',
                f'برای تایید ایمیل روی لینک زیر کلیک کنید:\n{verification_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except:
            raise serializers.ValidationError({"email": "ناموفق در ارسال ایمیل"})
        
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError("ایمیل موجود نیست")
        return value

    def send_password_reset_email(self, email):
        user = User.objects.get(email=email)
        reset_token = str(uuid.uuid4())
        
        user.token = reset_token
        user.token_created_at = timezone.now()
        user.save()
        request = self.context.get('request')
        reset_link = f"http://{request.get_host()}/accounts/password-reset-confirm/{reset_token}/"
        
        send_mail(
            'بازیابی رمز عبور',
            f'برای بازیابی رمز عبور روی لینک زیر کلیک کنید:\n{reset_link}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}
    )
    confirm_new_password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError({"password": "رمزهای عبور مطابقت ندارند"})
        
        try:
            user = User.objects.get(
                token=attrs['token'], 
                token_created_at__gt=timezone.now() - timezone.timedelta(hours=1)
            )
        except User.DoesNotExist:
            raise serializers.ValidationError({"token": "توکن نامعتبر یا منقضی شده است"})
        
        attrs['user'] = user
        return attrs

    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.token = None
        user.token_created_at = None
        user.save()
        return user
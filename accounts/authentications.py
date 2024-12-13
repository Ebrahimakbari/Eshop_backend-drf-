from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationBackend(BaseBackend):
    @classmethod
    def authenticate(self, email=None, password=None):
        user = User.objects.get(email=email)
        if user is not None and user.check_password(password) and user.is_active == True:
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
from django.conf import settings

from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken

class CookieJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get("access_token")
        if not access_token:
            return None

        try:
            # Проверяем токен
            validated_token = UntypedToken(access_token)
            user_id = validated_token["user_id"]
            user = User.objects.get(id=user_id)
            return user, validated_token
        except (InvalidToken, TokenError, User.DoesNotExist):
            raise AuthenticationFailed("Invalid token or user not found.")

from typing import Optional, Dict, Any

from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from auth_service import settings

from .services import UserService
from .serializers import UserSerializer


class RegisterView(APIView):
    def post(self, request: APIView) -> Response:
        username: str = request.data.get("username", "")
        password: str = request.data.get("password", "")
        service: UserService = UserService()
        user: User = service.register(username, password)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request: APIView) -> Response:
        username: str = request.data.get("username", "")
        password: str = request.data.get("password", "")
        service: UserService = UserService()
        user: Optional[User] = service.authenticate(username, password)

        if user:
            refresh : RefreshToken = RefreshToken.for_user(user)
            refresh["user_id"] = user.id
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = Response({"msg": "Login successful"})
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                value=access_token,
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                max_age=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds(),
            )
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                value=refresh_token,
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                max_age=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds(),
            )
            return response
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: APIView) -> Response:
        user: User = request.user
        return Response(UserSerializer(user).data)
    
    def patch(self, request: APIView) -> Response:
        user: User = request.user
        data: Dict[str, Any] = request.data
        service: UserService = UserService()
        updated_user: User = service.update_profile(user, **data)
        return Response(UserSerializer(updated_user).data)

class LogoutView(APIView):
    def post(self, request: APIView) -> Response:
        response = Response({"msg": "Logout successful"})
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])
        return response

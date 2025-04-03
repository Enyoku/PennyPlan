from typing import Optional
from urllib import request

from distlib.compat import Request
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from auth_service import settings

from .serializers import ChangePasswordSerializer, UserSerializer
from .services import UserService
from auth_service.auth_service.users import serializers


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
                key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
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
        if not request.user.is_authenticated:
            raise AuthenticationFailed("Authentication credentials were not provided.")
        user: User = request.user
        return Response(UserSerializer(user).data)

    def patch(self, request: APIView) -> Response:
        user: User = request.user
        serializer: UserSerializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request: APIView) -> Response:
        user: User = request.user
        service: UserService = UserService()
        service.delete_profile(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request: APIView) -> Response:
        user: User = request.user
        serializer = ChangePasswordSerializer(data=request.data, context={"user": user})

        if serializer.is_valid():
            user.set_password(serializer.validatedd_data["new_password"])
            user.save()
            return Response({"detail": "password changed successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request: APIView) -> Response:
        response = Response({"msg": "Logout successful"})
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])
        return response

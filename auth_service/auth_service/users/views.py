from typing import Optional, Dict, Any

from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .services import UserService
from .serializers import UserSerializer


class RegisterView(APIView):
    def post(self, request: APIView) -> Response:
        username: str = request.data.get("username", "")
        password: str = request.data.get("password", "")
        service: UserService = UserService()
        user: User = service.register(username, password)
        return Response(UserSerializer(user).data, status=201)
    
# TODO(add cookie support)
class LoginView(APIView):
    def post(self, request: APIView) -> Response:
        username: str = request.data.get("username", "")
        password: str = request.data.get("password", "")
        service: UserService = UserService()
        user: Optional[User] = service.authenticate(username, password)
        if user:
            refresh : RefreshToken = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=401)
    
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

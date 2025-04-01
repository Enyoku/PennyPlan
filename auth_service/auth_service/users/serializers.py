from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model: type[User] = User
        fields: list[str] = ["id", "username", "email"]

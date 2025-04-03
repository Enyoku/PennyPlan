from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model: type[User] = User
        fields: list[str] = ["id", "username", "email"]

    def validate_email(self, value: str) -> str:
        if not value:
            self.fail("empty_email", message="Email cannot be empty.")

        try:
            validate_email(value)
        except ValidationError:
            self.fail("Incorrect email format")

        if User.objects.filter(email=value).exclude(id=self.instance.id).exists():
            serializers.ValidationError("This email was already taken")

        return value

    def validate_username(self, value: str) -> str:
        if not value:
            raise serializers.ValidationError("Username cannot be empty")
        if len(value) < 3:
            raise serializers.ValidationError("Username must contain at least 3 characters")
        if User.objects.filter(username=value).exclude(id=self.instance.id).exists():
            self.fail("unique_email", message="This username has already taken")

        return value

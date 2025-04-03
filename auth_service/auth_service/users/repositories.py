from typing import Optional

from django.contrib.auth.models import User


class UserRepo:
    def get_user_by_username(self, username: str) -> Optional[User]:
        return User.objects.filter(username=username).first()

    def create_user(self, username: str, password: str) -> User:
        return User.objects.create_user(username=username, password=password)

    def update_user(self, user: User, **kwargs) -> User:
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save()
        return user

    def delete_user(self, user: User) -> None:
        user.delete()

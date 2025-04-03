from typing import Any, Dict, Optional

from django.contrib.auth.models import User

from .repositories import UserRepo


class UserService():
    def __init__(self) -> None:
        self.repo: UserRepo = UserRepo()

    def authenticate(self, username: str, password: str) -> Optional[User]:
        user: Optional[User] = self.repo.get_user_by_username(username)
        if user and user.check_password(password):  # Теперь user — экземпляр модели
            return user
        return None

    def register(self, username: str, password: str) -> User:
        return self.repo.create_user(username, password)

    def update_profile(self, user: User, **kwargs: Dict[str, Any]) -> User:
        return self.repo.update_user(user, **kwargs)

    def delete_profile(self, user: User) -> None:
        return self.repo.delete_user(user)

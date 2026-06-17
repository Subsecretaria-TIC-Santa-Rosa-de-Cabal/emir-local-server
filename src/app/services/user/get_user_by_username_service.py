from typing import Optional

from domain.entities.user import User
from domain.repositories.user_repository import UserRepository


def get_user_by_username_service(
    user_repository: UserRepository,
    username: str
) -> Optional[User]:
    return user_repository.get_by_username(username)

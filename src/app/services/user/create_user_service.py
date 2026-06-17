from typing import List, Optional, Tuple

from domain.entities.user import User
from domain.repositories.dto.user_dto import UserCreateDTO
from domain.repositories.user_repository import UserRepository


def create_user_service(
    user_repository: UserRepository,
    data: UserCreateDTO
) -> Optional[Tuple[List[User], int]]:
    return user_repository.create(data=data)

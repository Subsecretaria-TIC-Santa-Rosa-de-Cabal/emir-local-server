from typing import List, Optional, Tuple

from domain.entities.user import User
from domain.repositories.dto.user_dto import UserGetFilterDTO
from domain.repositories.user_repository import UserRepository


def get_users_service(
    user_repository: UserRepository,
    filter: UserGetFilterDTO
) -> Optional[Tuple[List[User], int]]:
    return user_repository.get(filter)

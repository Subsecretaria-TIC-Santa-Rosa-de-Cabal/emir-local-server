from typing import Optional
from uuid import UUID

from domain.entities.user import User
from domain.repositories.dto.user_dto import UserUpdateDTO
from domain.repositories.user_repository import UserRepository


def update_user_service(
    user_repository: UserRepository,
    identifier: UUID,
    data: UserUpdateDTO
) -> Optional[User]:
    return user_repository.update(
        identifier=identifier,
        data=data
    )

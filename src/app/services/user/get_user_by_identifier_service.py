from typing import Optional
from uuid import UUID

from domain.entities.user import User
from domain.repositories.user_repository import UserRepository


def get_user_by_identifier_service(
    user_repository: UserRepository,
    identifier: UUID
) -> Optional[User]:
    return user_repository.get_by_identifier(identifier)

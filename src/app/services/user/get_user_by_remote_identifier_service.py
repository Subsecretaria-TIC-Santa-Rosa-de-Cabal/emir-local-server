from typing import Optional
from uuid import UUID

from domain.entities.user import User
from domain.repositories.user_repository import UserRepository


def get_user_by_remote_identifier_service(
    user_repository: UserRepository,
    remote_identifier: UUID
) -> Optional[User]:
    return user_repository.get_by_remote_identifier(remote_identifier)

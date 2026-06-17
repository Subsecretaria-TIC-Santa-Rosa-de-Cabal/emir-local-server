from typing import Optional

from domain.entities.user import User
from domain.repositories.user_repository import UserRepository


def get_user_by_id_number_service(
    user_repository: UserRepository,
    id_number: str
) -> Optional[User]:
    return user_repository.get_by_id_number(id_number)

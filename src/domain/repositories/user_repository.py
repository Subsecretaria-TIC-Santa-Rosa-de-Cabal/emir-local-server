from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from uuid import UUID

from domain.repositories.dto.user_dto import UserCreateDTO, UserGetFilterDTO, UserUpdateDTO
from domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def get(self, filter: UserGetFilterDTO) -> Optional[Tuple[List[User], int]]:
        pass

    @abstractmethod
    def get_by_identifier(self, identifier: UUID) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_remote_identifier(self, remote_identifier: UUID) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_id_number(self, id_number: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def create(self, data: UserCreateDTO) -> Optional[User]:
        pass

    @abstractmethod
    def update(
        self,
        identifier: UUID,
        data: UserUpdateDTO
    ) -> Optional[User]:
        pass

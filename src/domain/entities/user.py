from datetime import datetime
from typing import Optional
from uuid import UUID

from domain.entities.base import Base


class User(Base):
    def __init__(
            self,
            identifier: UUID,
            enabled: bool,
            registration_date: datetime,
            last_update: datetime,
            remote_identifier: UUID,
            name: str,
            username: str,
            id_number: Optional[str] = None,
            phone_number: Optional[str] = None,
            email: Optional[str] = None
        ):
        super().__init__(
            identifier,
            enabled,
            registration_date,
            last_update,
        )
        self.__remote_identifier = remote_identifier
        self.__name = name
        self.__username = username
        self.__id_number = id_number
        self.__phone_number = phone_number
        self.__email = email

    @property
    def remote_identifier(self) -> UUID:
        return self.__remote_identifier
    
    @property
    def name(self) -> str:
        return self.__name

    @property
    def username(self) -> str:
        return self.__username

    @property
    def id_number(self) -> Optional[str]:
        return self.__id_number

    @property
    def phone_number(self) -> Optional[str]:
        return self.__phone_number

    @property
    def email(self) -> Optional[str]:
        return self.__email

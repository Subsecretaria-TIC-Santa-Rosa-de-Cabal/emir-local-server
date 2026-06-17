from datetime import datetime
from enum import Enum, unique
from typing import Optional
from uuid import UUID

from domain.entities.base import Base


@unique
class FileHashVersion(Enum):
    SHA256 = 'SHA256'
    SHA3_512 = 'SHA3_512'

class File(Base):
    def __init__(
            self,
            identifier: UUID,
            enabled: bool,
            registration_date: datetime,
            last_update: datetime,
            name: str,
            extension: str,
            route: str,
            size: int,
            hash: str,
            hash_version: FileHashVersion,
            created_by_identifier: UUID,
            observation: Optional[str] = None
        ):
        super().__init__(
            identifier,
            enabled,
            registration_date,
            last_update,
        )
        self.__name = name
        self.__extension = extension
        self.__route = route
        self.__size = size
        self.__hash = hash
        self.__hash_version = hash_version
        self.__created_by_identifier = created_by_identifier
        self.__observation = observation

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def extension(self) -> str:
        return self.__extension
    
    @property
    def route(self) -> str:
        return self.__route
    
    @property
    def size(self) -> int:
        return self.__size
    
    @property
    def hash(self) -> str:
        return self.__hash
    
    @property
    def hash_version(self) -> FileHashVersion:
        return self.__hash_version
    
    @property
    def created_by_identifier(self) -> UUID:
        return self.__created_by_identifier

    @property
    def observation(self) -> Optional[str]:
        return self.__observation

from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Optional
from uuid import UUID

from domain.entities.file import FileHashVersion
from domain.repositories.dto.types_dto import ToDictMixin


@unique
class FileOrderByOptions(Enum):
    REGISTRATION_DATE = 'REGISTRATION_DATE'
    NAME = 'NAME'
    EXTENSION = 'EXTENSION'
    SIZE = 'SIZE'

@dataclass
class FileGetFilterDTO:
    offset: Optional[int] = None
    limit: Optional[int] = None
    search: Optional[str] = None
    order_by: Optional[FileOrderByOptions] = None
    desc_order: Optional[bool] = True
    created_by_identifier: Optional[UUID] = None

@dataclass
class FileCreateDTO:
    name: str
    extension: str
    route: str
    size: int
    hash: str
    hash_version: FileHashVersion
    created_by_identifier: UUID
    observation: Optional[str] = None

@dataclass
class FileUpdateDTO(ToDictMixin):
    identifier: UUID
    name: Optional[str] = field(default=ToDictMixin._NOT_SENT)
    extension: Optional[str] = field(default=ToDictMixin._NOT_SENT)
    route: Optional[str] = field(default=ToDictMixin._NOT_SENT)
    size: Optional[int] = field(default=ToDictMixin._NOT_SENT)
    hash: Optional[str] = field(default=ToDictMixin._NOT_SENT)
    hash_version: Optional[FileHashVersion] = field(default=ToDictMixin._NOT_SENT)
    created_by_identifier: Optional[UUID] = field(default=ToDictMixin._NOT_SENT)
    observation: Optional[str] = field(default=ToDictMixin._NOT_SENT)

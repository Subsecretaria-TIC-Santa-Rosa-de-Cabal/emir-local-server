from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Optional
from uuid import UUID

from domain.repositories.dto.types_dto import ToDictMixin


@unique
class UserOrderByOptions(Enum):
    NAME = 'NAME'
    USERNAME = 'USERNAME'
    ID_NUMBER = 'ID_NUMBER'
    EMAIL = 'EMAIL'
    PHONE_NUMBER = 'PHONE_NUMBER'
    REGISTRATION_DATE = 'REGISTRATION_DATE'

@dataclass
class UserGetFilterDTO:
    offset: Optional[int] = None
    limit: Optional[int] = None
    search: Optional[str] = None
    order_by: Optional[UserOrderByOptions] = None
    desc_order: Optional[bool] = True

@dataclass
class UserCreateDTO:
    remote_identifier: UUID
    name: str
    username: str
    id_number: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None

@dataclass
class UserUpdateDTO(ToDictMixin):
    remote_identifier: Optional[UUID] = field(default=ToDictMixin._NOT_SENT)
    blocked: Optional[bool] = field(default=ToDictMixin._NOT_SENT)
    name: Optional[str] = field(default=ToDictMixin._NOT_SENT)
    username: Optional[str] = field(default=ToDictMixin._NOT_SENT)
    id_number: Optional[str] = field(default=ToDictMixin._NOT_SENT)
    phone_number: Optional[str] = field(default=ToDictMixin._NOT_SENT)
    email: Optional[str] = field(default=ToDictMixin._NOT_SENT)

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from domain.entities.file import FileHashVersion, File


class FileResponse(BaseModel):
    identifier: UUID
    enabled: bool
    registration_date: datetime
    last_update: datetime
    name: str
    extension: str
    route: str
    size: int
    hash: str
    hash_version: FileHashVersion
    created_by_identifier: UUID
    observation: Optional[str] = None

    @classmethod
    def from_domain(cls, file: File):
        return cls(
            identifier=file.identifier,
            enabled=file.enabled,
            registration_date=file.registration_date,
            last_update=file.last_update,
            name=file.name,
            extension=file.extension,
            route=file.route,
            size=file.size,
            hash=file.hash,
            hash_version=file.hash_version,
            created_by_identifier=file.created_by_identifier,
            observation=file.observation
        )

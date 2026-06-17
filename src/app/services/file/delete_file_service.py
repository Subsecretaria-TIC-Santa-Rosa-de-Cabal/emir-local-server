from typing import Optional
from uuid import UUID

from domain.entities.file import File
from domain.repositories.file_repository import FileRepository


def delete_file_service(
    file_repository: FileRepository,
    identifier: UUID
) -> Optional[File]:
    return file_repository.delete(identifier)

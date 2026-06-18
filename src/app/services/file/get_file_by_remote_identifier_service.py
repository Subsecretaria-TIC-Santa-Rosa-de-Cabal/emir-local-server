from typing import Optional
from uuid import UUID

from domain.entities.file import File
from domain.repositories.file_repository import FileRepository


def get_file_by_remote_identifier_service(
    file_repository: FileRepository,
    remote_identifier: UUID
) -> Optional[File]:
    return file_repository.get_by_remote_identifier(remote_identifier)

from typing import Optional

from domain.entities.file import File
from domain.repositories.dto.file_dto import FileUpdateDTO
from domain.repositories.file_repository import FileRepository


def update_file_service(
    file_repository: FileRepository,
    data: FileUpdateDTO
) -> Optional[File]:
    return file_repository.update(data)

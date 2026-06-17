from typing import Optional


from domain.entities.file import File
from domain.repositories.dto.file_dto import FileCreateDTO
from domain.repositories.file_repository import FileRepository


def create_file_service(
    file_repository: FileRepository,
    data: FileCreateDTO
) -> Optional[File]:
    return file_repository.create(data)

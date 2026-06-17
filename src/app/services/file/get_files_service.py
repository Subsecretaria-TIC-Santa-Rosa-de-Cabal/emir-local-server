from typing import List, Optional, Tuple

from domain.entities.file import File
from domain.repositories.dto.file_dto import FileGetFilterDTO
from domain.repositories.file_repository import FileRepository


def get_files_service(
    file_repository: FileRepository,
    filter: FileGetFilterDTO
) -> Optional[Tuple[List[File], int]]:
    return file_repository.get(filter)

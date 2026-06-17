from typing import BinaryIO

from domain.repositories.dto.storage_dto import SaveFileResponseDTO
from domain.repositories.storage_repository import StorageRepository


def save_file_service(
    storage_repository: StorageRepository,
    name: str,
    extension: str,
    path: str,
    file_body: BinaryIO
) -> SaveFileResponseDTO:
    return storage_repository.save_file(
        name,
        extension,
        path,
        file_body
    )

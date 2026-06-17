from domain.entities.file import File
from domain.repositories.storage_repository import StorageRepository


def delete_file_service(
    storage_repository: StorageRepository,
    file: File
) -> None:
    return storage_repository.delete_file(file)

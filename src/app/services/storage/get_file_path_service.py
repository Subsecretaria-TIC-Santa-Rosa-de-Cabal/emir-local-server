from domain.entities.file import File
from domain.repositories.storage_repository import StorageRepository


def get_file_path_service(
    storage_repository: StorageRepository,
    file: File
) -> str:
    return storage_repository.get_file_path(file)

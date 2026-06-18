from domain.repositories.storage_repository import StorageRepository


def is_base_folder_available_service(
    storage_repository: StorageRepository,
    folder_path: str
) -> bool:
    return storage_repository.is_base_folder_available(folder_path)

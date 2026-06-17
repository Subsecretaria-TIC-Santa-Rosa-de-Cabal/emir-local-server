from typing import BinaryIO

from app.services.storage.delete_file_service import delete_file_service
from app.services.storage.get_file_path_service import get_file_path_service
from app.services.storage.is_base_folder_available_service import is_base_folder_available_service
from app.services.storage.save_file_service import save_file_service
from domain.entities.file import File
from infrastructure.storage.local.repositories.local_storage_repository import LocalStorageRepository


class StorageFactory:
    @staticmethod
    def get_repository():
        repository = LocalStorageRepository()
        return repository
    
    @staticmethod
    def is_base_folder_available():
        return is_base_folder_available_service(
            storage_repository=StorageFactory.get_repository()
        )
        
    @staticmethod
    def get_file_path(file: File):
        return get_file_path_service(
            storage_repository=StorageFactory.get_repository(),
            file=file
        )
    
    @staticmethod
    def delete_file(file: File):
        return delete_file_service(
            storage_repository=StorageFactory.get_repository(),
            file=file
        )
    
    @staticmethod
    def save_file(
        name: str,
        extension: str,
        path: str,
        file_body: BinaryIO
    ):
        return save_file_service(
            storage_repository=StorageFactory.get_repository(),
            name=name,
            extension=extension,
            path=path,
            file_body=file_body
        )

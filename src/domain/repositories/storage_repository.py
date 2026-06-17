from abc import ABC, abstractmethod
from typing import BinaryIO

from domain.entities.file import File
from domain.repositories.dto.storage_dto import SaveFileResponseDTO


class StorageRepository(ABC):
    @abstractmethod
    def is_base_folder_available(
        self
    ) -> bool:
        pass
    
    @abstractmethod
    def save_file(
        self,
        name: str,
        extension: str,
        path: str,
        file_body: BinaryIO
    ) -> SaveFileResponseDTO:
        pass

    @abstractmethod
    def get_file_path(
        self,
        file: File
    ) -> str:
        pass

    @abstractmethod
    def delete_file(
        self,
        file: File
    ) -> None:
        pass

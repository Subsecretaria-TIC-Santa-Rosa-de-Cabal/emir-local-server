import os
import shutil
from typing import BinaryIO
from uuid import uuid4

from domain.entities.file import File
from domain.repositories.dto.storage_dto import SaveFileResponseDTO
from domain.repositories.storage_repository import StorageRepository
from infrastructure.storage.local.config import BASE_PATH


class LocalStorageRepository(StorageRepository):
    def __init__(self):
        self.base_path = BASE_PATH

    def is_base_folder_available(
        self
    ) -> bool:
        try:
            if not os.path.isdir(self.base_path):
                return False

            if not os.access(self.base_path, os.R_OK | os.W_OK):
                return False

            test_file = os.path.join(self.base_path, f".{uuid4()}.tmp")
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)

            return True
        except Exception:
            return False

    def save_file(
        self,
        name: str,
        extension: str,
        path: str,
        file_body: BinaryIO
    ) -> SaveFileResponseDTO:
        final_path = os.path.join(self.base_path, path, name + '.' + extension)

        os.makedirs(os.path.dirname(final_path), exist_ok=True)

        with open(final_path, "wb") as f:
            f.write(file_body)

        return SaveFileResponseDTO(
            absolute_path=final_path
        )
    
    def get_file_path(
        self,
        file: File
    ) -> str:
        return file.route
    
    def delete_file(
        self,
        file: File
    ) -> None:
        os.remove(file.route)

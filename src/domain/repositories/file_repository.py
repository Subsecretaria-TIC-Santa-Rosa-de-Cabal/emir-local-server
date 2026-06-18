from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from uuid import UUID

from domain.entities.file import File
from domain.repositories.dto.file_dto import FileCreateDTO, FileGetFilterDTO, FileUpdateDTO


class FileRepository(ABC):
    @abstractmethod
    def get(self, filter: FileGetFilterDTO) -> Optional[Tuple[List[File], int]]:
        pass

    @abstractmethod
    def get_by_identifier(self, identifier: UUID) -> Optional[File]:
        pass

    @abstractmethod
    def get_by_remote_identifier(self, remote_identifier: UUID) -> Optional[File]:
        pass

    @abstractmethod
    def create(self, data: FileCreateDTO) -> Optional[File]:
        pass

    @abstractmethod
    def update(
        self,
        data: FileUpdateDTO
    ) -> Optional[File]:
        pass

    @abstractmethod
    def delete(
        self,
        identifier: UUID
    ) -> Optional[File]:
        pass

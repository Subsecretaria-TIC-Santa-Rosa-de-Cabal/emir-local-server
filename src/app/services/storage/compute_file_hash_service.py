from typing import BinaryIO

from domain.entities.file import FileHashVersion
from domain.repositories.storage_repository import StorageRepository


def compute_file_hash_service(
    storage_repository: StorageRepository,
    hash_version: FileHashVersion,
    file_body: BinaryIO
) -> str:
    return storage_repository.compute_file_hash(hash_version, file_body)

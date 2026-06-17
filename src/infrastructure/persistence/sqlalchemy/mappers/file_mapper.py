from domain.entities.file import File, FileHashVersion
from infrastructure.persistence.sqlalchemy.models.file_model import FileModel


class FileMapper:
    @staticmethod
    def to_domain(file_model: FileModel) -> File:
        return File(
            identifier = file_model.id,
            enabled = file_model.enabled,
            registration_date = file_model.registration_date,
            last_update = file_model.last_update,
            name = file_model.name,
            extension = file_model.extension,
            route = file_model.route,
            size = file_model.size,
            hash = file_model.hash,
            hash_version = FileHashVersion(file_model.hash_version),
            created_by_identifier = file_model.created_by_id,
            observation = file_model.observation,
        )

    @staticmethod
    def to_model(file: File) -> FileModel:
        return FileModel(
            id = file.identifier,
            enabled = file.enabled,
            registration_date = file.registration_date,
            last_update = file.last_update,
            name = file.name,
            extension = file.extension,
            route = file.route,
            size = file.size,
            hash = file.hash,
            hash_version = file.hash_version.value,
            created_by_id = file.created_by_identifier,
            observation = file.observation,
        )

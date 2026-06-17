from uuid import UUID

from app.services.file.create_file_service import create_file_service
from app.services.file.delete_file_service import delete_file_service
from app.services.file.get_file_by_identifier_service import get_file_by_identifier_service
from app.services.file.get_files_service import get_files_service
from app.services.file.update_file_service import update_file_service
from domain.repositories.dto.file_dto import FileCreateDTO, FileGetFilterDTO, FileUpdateDTO
from infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_file_repository import SQLAlchemyFileRepository


class FileFactory:
    @staticmethod
    def get_repository(session):
        repository = SQLAlchemyFileRepository(session)
        return repository

    @staticmethod
    def get_files(session, filter: FileGetFilterDTO):
        return get_files_service(
            file_repository=FileFactory.get_repository(session),
            filter=filter
        )

    @staticmethod
    def get_file_by_identifier(session, identifier: UUID):
        return get_file_by_identifier_service(
            file_repository=FileFactory.get_repository(session),
            identifier=identifier
        )

    @staticmethod
    def create_file(session, data: FileCreateDTO):
        return create_file_service(
            file_repository=FileFactory.get_repository(session),
            data=data
        )

    @staticmethod
    def update_file(session, data: FileUpdateDTO):
        return update_file_service(
            file_repository=FileFactory.get_repository(session),
            data=data
        )
    
    @staticmethod
    def delete_file(session, identifier: UUID):
        return delete_file_service(
            file_repository=FileFactory.get_repository(session),
            identifier=identifier
        )

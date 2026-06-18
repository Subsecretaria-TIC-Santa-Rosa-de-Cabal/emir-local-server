from typing import List, Optional, Tuple
from uuid import UUID

from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

from domain.entities.file import File
from domain.repositories.dto.file_dto import FileCreateDTO, FileGetFilterDTO, FileUpdateDTO
from domain.repositories.file_repository import FileRepository
from infrastructure.persistence.sqlalchemy.mappers.file_mapper import FileMapper
from infrastructure.persistence.sqlalchemy.models.file_model import FileModel


class SQLAlchemyFileRepository(FileRepository):
    def __init__(self, session: Session):
        self.session = session

    def get(self, filter: FileGetFilterDTO) -> Optional[Tuple[List[File], int]]:
        query = self.session.query(FileModel).filter_by(enabled=True)

        if filter.created_by_identifier is not None:
            query = query.filter_by(created_by_id=filter.created_by_identifier)

        if filter.search is not None:
            search_pattern = f"%{filter.search}%"
            query = query.filter(
                or_(
                    FileModel.name.ilike(search_pattern),
                )
            )

        if filter.order_by is not None:
            field = None
            if filter.order_by == FileModel.REGISTRATION_DATE:
                field = FileModel.registration_date
            elif filter.order_by == FileModel.NAME:
                field = FileModel.name
            elif filter.order_by == FileModel.EXTENSION:
                field = FileModel.extension
            elif filter.order_by == FileModel.SIZE:
                field = FileModel.size

            if field is not None:
                if filter.desc_order is True:
                    field = desc(field)
                else:
                    field = asc(field)
                query = query.order_by(field)

        total = query.count()

        if filter.offset is not None:
            query =  query.offset(filter.offset)
        if filter.limit is not None:
            query =  query.limit(filter.limit)

        file_models = query.all()
        if not file_models:
            return [], 0
        
        return [FileMapper.to_domain(file_model) for file_model in file_models], total
    
    def get_by_identifier(self, identifier: UUID) -> Optional[File]:
        file_model = self.session.query(FileModel).filter_by(
            id=identifier,
            enabled=True
        ).first()
        if file_model:
            return FileMapper.to_domain(file_model)
        return None
    
    def get_by_remote_identifier(self, remote_identifier: UUID) -> Optional[File]:
        file_model = self.session.query(FileModel).filter_by(
            remote_id=remote_identifier,
            enabled=True
        ).first()
        if file_model:
            return FileMapper.to_domain(file_model)
        return None

    def create(self, data: FileCreateDTO) -> Optional[File]:
        new_file = FileModel(
            remote_id=data.remote_identifier,
            name=data.name,
            extension=data.extension,
            route=data.route,
            size=data.size,
            hash=data.hash,
            hash_version=data.hash_version.value,
            created_by_id=data.created_by_identifier,
            observation=data.observation
        )
        self.session.add(new_file)
        self.session.commit()
        return FileMapper.to_domain(new_file)

    def update(
        self,
        data: FileUpdateDTO
    ) -> Optional[File]:
        payload = data.to_dict()
        identifier = payload['identifier']
        del payload['identifier']

        if 'hash_version' in payload:
            payload['hash_version'] = payload['hash_version'].value

        if 'created_by_identifier' in payload:
            payload['created_by_id'] = payload['created_by_identifier']
            del payload['created_by_identifier']

        if 'remote_identifier' in payload:
            payload['remote_id'] = payload['remote_identifier']
            del payload['remote_identifier']

        self.session.query(FileModel).filter(
            FileModel.id == identifier
        ).update(payload, synchronize_session="fetch")
        self.session.commit()
        return self.get_by_identifier(identifier)
    
    def delete(
        self,
        identifier: UUID
    ) -> Optional[File]:
        file_model = self.session.query(FileModel).filter_by(
            id=identifier
        ).first()
        self.session.delete(file_model)
        self.session.commit()
        return FileMapper.to_domain(file_model)

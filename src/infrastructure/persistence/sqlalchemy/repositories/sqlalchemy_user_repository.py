from typing import List, Optional, Tuple
from uuid import UUID

from sqlalchemy import or_, asc, desc
from sqlalchemy.orm import Session

from domain.entities.user import User
from domain.repositories.dto.user_dto import UserCreateDTO, UserGetFilterDTO, UserOrderByOptions, UserUpdateDTO
from domain.repositories.user_repository import UserRepository
from infrastructure.persistence.sqlalchemy.mappers.user_mapper import UserMapper
from infrastructure.persistence.sqlalchemy.models.user_model import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session
    
    def get(self, filter: UserGetFilterDTO) -> Optional[Tuple[List[User], int]]:
        query = self.session.query(UserModel).filter_by(enabled=True)

        if filter.search is not None:
            search_pattern = f"%{filter.search}%"
            query = query.filter(
                or_(
                    UserModel.name.ilike(search_pattern),
                    UserModel.username.ilike(search_pattern),
                    UserModel.id_number.ilike(search_pattern),
                    UserModel.email.ilike(search_pattern),
                    UserModel.phone_number.ilike(search_pattern),
                )
            )

        if filter.order_by is not None:
            field = None
            if filter.order_by == UserOrderByOptions.ID_NUMBER:
                field = UserModel.id_number
            elif filter.order_by == UserOrderByOptions.NAME:
                field = UserModel.name
            elif filter.order_by == UserOrderByOptions.USERNAME:
                field = UserModel.username
            elif filter.order_by == UserOrderByOptions.EMAIL:
                field = UserModel.email
            elif filter.order_by == UserOrderByOptions.PHONE_NUMBER:
                field = UserModel.phone_number
            elif filter.order_by == UserOrderByOptions.REGISTRATION_DATE:
                field = UserModel.registration_date

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

        user_models = query.all()
        if not user_models:
            return [], 0
        
        return [UserMapper.to_domain(user_model) for user_model in user_models], total
    
    def get_by_identifier(self, identifier: UUID) -> Optional[User]:
        user_model = self.session.query(UserModel).filter_by(
            id=identifier,
            enabled=True
        ).first()
        if user_model:
            return UserMapper.to_domain(user_model)
        return None
    
    def get_by_remote_identifier(self, remote_identifier: UUID) -> Optional[User]:
        user_model = self.session.query(UserModel).filter_by(
            remote_id=remote_identifier,
            enabled=True
        ).first()
        if user_model:
            return UserMapper.to_domain(user_model)
        return None
    
    def get_by_username(self, username: str) -> Optional[User]:
        user_model = self.session.query(UserModel).filter_by(
            username=username,
            enabled=True
        ).first()
        if user_model:
            return UserMapper.to_domain(user_model)
        return None
    
    def get_by_id_number(self, id_number: str) -> Optional[User]:
        user_model = self.session.query(UserModel).filter_by(
            id_number=id_number,
            enabled=True
        ).first()
        if user_model:
            return UserMapper.to_domain(user_model)
        return None
    
    def get_by_email(self, email: str) -> Optional[User]:
        user_model = self.session.query(UserModel).filter_by(
            email=email,
            enabled=True
        ).first()
        if user_model:
            return UserMapper.to_domain(user_model)
        return None
    
    def create(self, data: UserCreateDTO) -> Optional[User]:
        new_user = UserModel(
            remote_id=data.remote_identifier,
            name=data.name,
            username=data.username,
            id_number=data.id_number,
            phone_number=data.phone_number,
            email=data.email
        )
        self.session.add(new_user)
        self.session.commit()
        return UserMapper.to_domain(new_user)
    
    def update(
        self,
        identifier: UUID,
        data: UserUpdateDTO
    ) -> Optional[User]:
        payload = data.to_dict()

        if 'remote_identifier' in payload:
            payload['remote_id'] = 'remote_identifier'
            del payload['remote_identifier']

        self.session.query(UserModel).filter(
            UserModel.id == identifier
        ).update(payload, synchronize_session="fetch")
        self.session.commit()
        return self.get_by_identifier(identifier)

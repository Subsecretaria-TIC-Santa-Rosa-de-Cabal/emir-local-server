from uuid import UUID

from app.services.user.create_user_service import create_user_service
from app.services.user.get_user_by_email_service import get_user_by_email_service
from app.services.user.get_user_by_id_number_service import get_user_by_id_number_service
from app.services.user.get_user_by_identifier_service import get_user_by_identifier_service
from app.services.user.get_user_by_username_service import get_user_by_username_service
from app.services.user.get_users_service import get_users_service
from app.services.user.update_user_service import update_user_service
from domain.repositories.dto.user_dto import UserCreateDTO, UserGetFilterDTO, UserUpdateDTO
from infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository


class UserFactory:
    @staticmethod
    def get_repository(session):
        repository = SQLAlchemyUserRepository(session)
        return repository

    @staticmethod
    def get_users(session, filter: UserGetFilterDTO):
        return get_users_service(
            user_repository=UserFactory.get_repository(session),
            filter=filter
        )

    @staticmethod
    def get_user_by_identifier(session, identifier: UUID):
        return get_user_by_identifier_service(
            user_repository=UserFactory.get_repository(session),
            identifier=identifier
        )
    
    @staticmethod
    def get_user_by_username(session, username: str):
        return get_user_by_username_service(
            user_repository=UserFactory.get_repository(session),
            username=username
        )
    
    @staticmethod
    def get_user_by_id_number(session, id_number: str):
        return get_user_by_id_number_service(
            user_repository=UserFactory.get_repository(session),
            id_number=id_number
        )
    
    @staticmethod
    def get_user_by_email(session, email: str):
        return get_user_by_email_service(
            user_repository=UserFactory.get_repository(session),
            email=email
        )
    
    @staticmethod
    def create_user(session, data: UserCreateDTO):
        return create_user_service(
            user_repository=UserFactory.get_repository(session),
            data=data
        )
    
    @staticmethod
    def update_user(session, identifier: UUID, data: UserUpdateDTO):
        return update_user_service(
            user_repository=UserFactory.get_repository(session),
            identifier=identifier,
            data=data
        )

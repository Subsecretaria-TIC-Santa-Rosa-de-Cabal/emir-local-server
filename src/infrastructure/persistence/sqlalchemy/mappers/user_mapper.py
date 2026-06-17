from domain.entities.user import User
from infrastructure.persistence.sqlalchemy.models.user_model import UserModel


class UserMapper:
    @staticmethod
    def to_domain(user_model: UserModel) -> User:
        return User(
            identifier = user_model.id,
            enabled = user_model.enabled,
            registration_date = user_model.registration_date,
            last_update = user_model.last_update,
            name = user_model.name,
            username = user_model.username,
            id_number = user_model.id_number,
            phone_number = user_model.phone_number,
            email = user_model.email
        )

    @staticmethod
    def to_model(user: User) -> UserModel:
        return UserModel(
            id = user.identifier,
            enabled = user.enabled,
            registration_date = user.registration_date,
            last_update = user.last_update,
            name = user.name,
            username = user.username,
            id_number = user.id_number,
            phone_number = user.phone_number,
            email = user.email
        )

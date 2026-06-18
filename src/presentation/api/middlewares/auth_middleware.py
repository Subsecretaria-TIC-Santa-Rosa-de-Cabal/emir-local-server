import base64
from dataclasses import dataclass
import os
from typing import Optional
import uuid

from dotenv import load_dotenv
from fastapi import Depends, Security
from fastapi.security import APIKeyHeader
import jwt

from app.factories.user_factory import UserFactory
from domain.entities.user import User
from domain.repositories.dto.user_dto import UserCreateDTO
from presentation.api.deps import get_db
from presentation.api.exceptions.fastapi_authentication_exceptions import AccessDenied, AccessTokenExpired, UserNotAuthenticated


load_dotenv()
PUBLIC_KEY = base64.b64decode(os.getenv("EMIR_PUBLIC_KEY_BASE64"))
JWT_ISS = os.getenv("JWT_ISS")
JWT_AUD = os.getenv("JWT_AUD")

@dataclass
class AuthResponse:
    user: User
    role_codes: list[str]
    body: Optional[dict]

async def verify_jwt(
    authorization_header_value: str = Security(APIKeyHeader(name="Authorization")),
    session = Depends(get_db),
) -> AuthResponse:
    if not authorization_header_value or 'Bearer ' not in authorization_header_value:
        raise UserNotAuthenticated()

    access_token = authorization_header_value.split('Bearer ')[-1]

    try:
        payload = jwt.decode(
            access_token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            options={"require": ["exp", "iss", "aud", "role_codes", "user"]},
            audience=JWT_AUD,
            issuer=JWT_ISS
        )
        remote_identifier = uuid.UUID(payload['user']['remote_identifier'])
        auth_user = UserFactory.get_user_by_remote_identifier(
            session=session,
            remote_identifier=remote_identifier
        )
        if not auth_user:
            auth_user = UserFactory.create_user(
                session=session,
                data=UserCreateDTO(
                    remote_identifier=remote_identifier,
                    name=payload['user']['name'],
                    username=payload['user']['username'],
                    id_number=payload['user']['id_number'],
                    phone_number=payload['user']['phone_number'],
                    email=payload['user']['email'],
                )
            )
        auth_response = AuthResponse(
            user=auth_user,
            role_codes=payload['role_codes'],
            body=payload['body']
        )
        return auth_response

    except jwt.ExpiredSignatureError:
        raise AccessTokenExpired()
    except jwt.InvalidTokenError as e:
        raise UserNotAuthenticated()

def authorize_route(current_roles: list[str], required_role_codes: list[str]):
    if not any(elem in required_role_codes for elem in current_roles):
        raise AccessDenied()

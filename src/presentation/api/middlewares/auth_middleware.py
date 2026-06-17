from fastapi import Security
from fastapi.security import APIKeyHeader
import jwt

from presentation.api.exceptions.fastapi_authentication_exceptions import AccessTokenExpired, UserNotAuthenticated


async def verify_jwt(
    authorization_header_value: str = Security(APIKeyHeader(name="Authorization"))
):
    if not authorization_header_value or 'Bearer ' not in authorization_header_value:
        raise UserNotAuthenticated()
    
    access_token = authorization_header_value.split('Bearer ')[-1]

    with open("keys/public.pem", "rb") as f:
        public_key = f.read()

    try:
        payload = jwt.decode(
            access_token,
            public_key,
            algorithms=["RS256"]
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise AccessTokenExpired()
    except jwt.InvalidTokenError as e:
        raise UserNotAuthenticated()

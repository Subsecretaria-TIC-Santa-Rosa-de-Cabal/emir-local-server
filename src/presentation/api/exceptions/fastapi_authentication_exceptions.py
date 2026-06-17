from presentation.api.exceptions.fastapi_exceptions import AppError


class UserNotAuthenticated(AppError):
    def __init__(self):
        super().__init__(1000, "User not authenticated", 401)

class AccessTokenExpired(AppError):
    def __init__(self):
        super().__init__(1001, "Access token expired", 403)

class AccessDenied(AppError):
    def __init__(self):
        super().__init__(1002, "Access denied", 403)


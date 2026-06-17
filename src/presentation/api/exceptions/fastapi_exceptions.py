from fastapi import HTTPException

class AppError(HTTPException):
    def __init__(
            self,
            error_code: int,
            message: str,
            status_code: int = 400,
            data: dict = None
        ):
        super().__init__(
            status_code=status_code,
            detail={
                "error_code": error_code,
                "message": message,
                "data": data
            }
        )

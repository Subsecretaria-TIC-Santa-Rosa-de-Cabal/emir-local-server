from presentation.api.exceptions.fastapi_exceptions import AppError


class FileExtensionNotAllowed(AppError):
    def __init__(self):
        super().__init__(2000, "File extension not allowed", 400)

class FileInvalidSize(AppError):
    def __init__(self):
        super().__init__(2001, "The file size is invalid", 400)

class FileInvalidChecksum(AppError):
    def __init__(self):
        super().__init__(2002, "The file checksum is invalid", 400)

class BaseFolderUnavailable(AppError):
    def __init__(self):
        super().__init__(2003, "The base folder is unavailable", 400)

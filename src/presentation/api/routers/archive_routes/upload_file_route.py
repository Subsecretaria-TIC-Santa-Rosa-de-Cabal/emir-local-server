import hashlib

from fastapi import APIRouter, Depends, File, UploadFile

from app.factories.file_factory import FileFactory
from app.factories.storage_factory import StorageFactory
from app.factories.user_factory import UserFactory
from domain.entities.file import FileHashVersion
from domain.repositories.dto.file_dto import FileCreateDTO
from domain.repositories.dto.user_dto import UserCreateDTO
from presentation.api.deps import get_db
from presentation.api.middlewares.auth_middleware import verify_jwt
from presentation.api.exceptions.fastapi_archive_exceptions import BaseFolderUnavailable, FileExtensionNotAllowed, FileInvalidChecksum, FileInvalidSize
from presentation.api.schemas.file_schema import FileResponse


upload_file_router = APIRouter()

@upload_file_router.post('/upload_file', response_model=FileResponse)
async def upload_file(
    session = Depends(get_db),
    payload = Depends(verify_jwt),
    file: UploadFile = File(...)
):
    if not StorageFactory.is_base_folder_available():
        raise BaseFolderUnavailable()

    current_user = UserFactory.get_user_by_username(
        session=session,
        username=payload['user']['username']
    )
    if not current_user:
        current_user = UserFactory.create_user(
            session=session,
            data=UserCreateDTO(
                name=payload['user']['name'],
                username=payload['user']['username'],
                id_number=payload['user']['id_number'],
                phone_number=payload['user']['phone_number'],
                email=payload['user']['email'],
            )
        )

    file_extension = file.filename.split('.')[-1].lower()
    if file_extension != payload['file']['extension']:
        raise FileExtensionNotAllowed()
    
    content = await file.read()
    
    checksum = hashlib.sha256(content).hexdigest()
    if payload['file']['checksum'] != checksum:
        raise FileInvalidChecksum()
    
    if len(content) != payload['file']['size']:
        raise FileInvalidSize()
    
    file_response = StorageFactory.save_file(
        name=payload['file']['name'],
        extension=payload['file']['extension'],
        path='apps/archive',
        file_body=content
    )

    new_file = FileFactory.create_file(
        session=session,
        data=FileCreateDTO(
            name=payload['file']['name'],
            extension=payload['file']['extension'],
            route=file_response.absolute_path,
            size=payload['file']['size'],
            hash=payload['file']['checksum'],
            hash_version=FileHashVersion.SHA256,
            created_by_identifier=current_user.identifier,
            observation=payload['file']['observation'],
        )
    )

    return FileResponse.from_domain(new_file)

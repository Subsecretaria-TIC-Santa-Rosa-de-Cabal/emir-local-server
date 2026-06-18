import hashlib
import uuid

from fastapi import APIRouter, Depends, File, UploadFile

from app.factories.file_factory import FileFactory
from app.factories.storage_factory import StorageFactory
from domain.entities.file import FileHashVersion
from domain.repositories.dto.file_dto import FileCreateDTO
from presentation.api.deps import get_db
from presentation.api.middlewares.auth_middleware import verify_jwt
from presentation.api.exceptions.fastapi_archive_exceptions import BaseFolderUnavailable, FileExtensionNotAllowed, FileInvalidChecksum, FileInvalidSize
from presentation.api.schemas.file_schema import FileResponse


upload_file_router = APIRouter()

@upload_file_router.post('/file/upload', response_model=FileResponse)
async def upload_file(
    session = Depends(get_db),
    auth = Depends(verify_jwt),
    file: UploadFile = File(...)
):
    if not StorageFactory.is_base_folder_available():
        raise BaseFolderUnavailable()

    remote_identifier = uuid.UUID(auth.body['file']['remote_identifier'])
    current_file = FileFactory.get_file_by_remote_identifier(
        session=session,
        remote_identifier=remote_identifier
    )
    if current_file:
        return FileResponse.from_domain(current_file)

    file_extension = file.filename.split('.')[-1].lower()
    if file_extension != auth.body['file']['extension']:
        raise FileExtensionNotAllowed()
    
    content = await file.read()
    
    checksum = hashlib.sha256(content).hexdigest()
    if auth.body['file']['checksum'] != checksum:
        raise FileInvalidChecksum()
    
    if len(content) != auth.body['file']['size']:
        raise FileInvalidSize()
    
    file_response = StorageFactory.save_file(
        name=auth.body['file']['name'],
        extension=auth.body['file']['extension'],
        path='apps/archive',
        file_body=content
    )

    new_file = FileFactory.create_file(
        session=session,
        data=FileCreateDTO(
            remote_identifier=remote_identifier,
            name=auth.body['file']['name'],
            extension=auth.body['file']['extension'],
            route=file_response.absolute_path,
            size=auth.body['file']['size'],
            hash=auth.body['file']['checksum'],
            hash_version=FileHashVersion.SHA256,
            created_by_identifier=auth.user.identifier,
            observation=auth.body['file']['observation'],
        )
    )

    return FileResponse.from_domain(new_file)

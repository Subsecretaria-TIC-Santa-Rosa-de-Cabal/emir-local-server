import hashlib
import os
import uuid

from fastapi import APIRouter, Depends, File, UploadFile

from app.factories.file_factory import FileFactory
from app.factories.storage_factory import StorageFactory
from domain.entities.file import FileHashVersion
from domain.repositories.dto.file_dto import FileCreateDTO
from presentation.api.deps import get_db
from presentation.api.middlewares.auth_middleware import authorize_route, verify_jwt
from presentation.api.exceptions.fastapi_archive_exceptions import BaseFolderUnavailable, FileExtensionNotAllowed, FileInvalidChecksum, FileInvalidSize
from presentation.api.schemas.file_schema import FileResponse


upload_file_router = APIRouter()

@upload_file_router.post('/file/upload', response_model=FileResponse)
async def upload_file(
    session = Depends(get_db),
    auth = Depends(verify_jwt),
    file: UploadFile = File(...)
):
    ARCHIVE_MAIN_FOLDER = os.getenv('ARCHIVE_MAIN_FOLDER')
    if not StorageFactory.is_base_folder_available(ARCHIVE_MAIN_FOLDER):
        raise BaseFolderUnavailable()
    
    authorize_route(auth.role_codes, ['SUPER_ADMIN', 'ARCHIVE_BASE'])

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
    
    file_hash = StorageFactory.compute_file_hash(
        hash_version=FileHashVersion(auth.body['file']['hash_version']),
        file_body=content
    )
    if auth.body['file']['hash'] != file_hash:
        raise FileInvalidChecksum()
    
    if len(content) != auth.body['file']['size']:
        raise FileInvalidSize()
    
    full_path = os.path.join(ARCHIVE_MAIN_FOLDER, auth.body['file']['remote_route'])
    file_response = StorageFactory.save_file(
        name=auth.body['file']['name'],
        extension=auth.body['file']['extension'],
        path=full_path,
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
            hash=auth.body['file']['hash'],
            hash_version=FileHashVersion(auth.body['file']['hash_version']),
            created_by_identifier=auth.user.identifier,
            observation=auth.body['file']['observation'],
        )
    )

    return FileResponse.from_domain(new_file)

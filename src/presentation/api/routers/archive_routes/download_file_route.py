import os
import uuid

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse as FastapiFileResponse

from app.factories.file_factory import FileFactory
from app.factories.storage_factory import StorageFactory
from presentation.api.deps import get_db
from presentation.api.middlewares.auth_middleware import authorize_route, verify_jwt
from presentation.api.exceptions.fastapi_archive_exceptions import BaseFolderUnavailable, FileNotExist


download_file_router = APIRouter()

@download_file_router.post('/file/download')
async def download_file(
    session = Depends(get_db),
    auth = Depends(verify_jwt)
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
    if not current_file:
        raise FileNotExist()

    return FastapiFileResponse(
        path=current_file.route,
        filename=current_file.name+'.'+current_file.extension
    )

import os

from fastapi import APIRouter

from app.factories.storage_factory import StorageFactory


is_available_router = APIRouter()

@is_available_router.get('/is_available', response_model=bool)
async def is_available():
    ARCHIVE_MAIN_FOLDER = os.getenv('ARCHIVE_MAIN_FOLDER')
    return StorageFactory.is_base_folder_available(ARCHIVE_MAIN_FOLDER)

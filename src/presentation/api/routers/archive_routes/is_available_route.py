from fastapi import APIRouter

from app.factories.storage_factory import StorageFactory


is_available_router = APIRouter()

@is_available_router.get('/is_available', response_model=bool)
async def is_available():
    return StorageFactory.is_base_folder_available()

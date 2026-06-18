from fastapi import APIRouter

from presentation.api.routers.archive_routes.is_available_route import is_available_router
from presentation.api.routers.archive_routes.upload_file_route import upload_file_router
from presentation.api.routers.archive_routes.download_file_route import download_file_router


archive_router = APIRouter()

archive_router.include_router(is_available_router)
archive_router.include_router(upload_file_router)
archive_router.include_router(download_file_router)

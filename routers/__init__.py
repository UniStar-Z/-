from .data_collection import router as data_collection_router
from .user_interface import router as user_interface_router
from .data_management import router as data_management_router
from .image_upload import router as image_upload_router

# 显式导出列表（非必须但推荐）
__all__ = [
    "data_collection_router",
    "user_interface_router",
    "data_management_router",
    "image_upload_router"
]
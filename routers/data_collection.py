from fastapi import APIRouter
from data_collection.collection import get_all_defect_data,convert_data_format

router = APIRouter()

router.add_api_route(
    "/get_all_data",
    get_all_defect_data,
    methods=["GET"]
)

router.add_api_route(
    "/convert_format",
    convert_data_format,
    methods=["POST"]
)